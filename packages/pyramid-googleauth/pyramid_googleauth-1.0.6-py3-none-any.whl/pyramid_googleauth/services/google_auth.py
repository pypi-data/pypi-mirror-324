import base64
import json
import os
import random
from datetime import datetime, timedelta
from urllib.parse import parse_qsl, urlparse

import jwt
from google_auth_oauthlib.flow import Flow
from jwt import InvalidTokenError
from oauthlib.oauth2.rfc6749.errors import InvalidClientError, InvalidGrantError

from pyramid_googleauth.exceptions import BadOAuth2Config, UserNotAuthenticated


class GoogleAuthService:
    # https://developers.google.com/identity/protocols/oauth2/web-server

    # From: https://accounts.google.com/.well-known/openid-configuration

    NONCE_EXPIRATION = timedelta(minutes=60)

    HEX_DIGITS = "012345678abcdef"

    SALT_LENGTH = 32

    OPEN_ID_DISCOVERY = {
        "authorization_endpoint": "https://accounts.google.com/o/oauth2/v2/auth",
        "token_endpoint": "https://oauth2.googleapis.com/token",
    }

    SCOPES = [
        # Get the email address we will use for the user id
        "https://www.googleapis.com/auth/userinfo.email",
        # Get additional "nice to have" things like the name and picture
        "https://www.googleapis.com/auth/userinfo.profile",
        # This is a default, but includes getting any id info at all
        "openid",
    ]

    def __init__(self, secret, client_config):
        """Create a new authentication service object.

        :param secret: Secret used for nonce generation
        :param client_config: Dict of Google OAuth2 configuration data

        Expected keys of `client_config`:

            * `client_id` - Google provided client id for this environment
            * `client_secret` - Secret which matches the `client_id`
            * `redirect_uri` - Redirect URI registered with Google
        """

        self._secret = secret

        self._client_id = client_config["client_id"]
        self._client_secret = client_config["client_secret"]
        self._redirect_uri = client_config["redirect_uri"]

        if not self._redirect_uri.startswith("https"):
            # Allow HTTP in dev, otherwise we'll get errors when trying to
            # authenticate with some of the OAuth libraries
            os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    def _encode_state(self, payload: dict):
        return base64.urlsafe_b64encode(json.dumps(payload).encode("utf8"))

    def _decode_state(self, state: str):
        try:
            return json.loads(base64.urlsafe_b64decode(state))
        except ValueError:
            return {}

    def _get_nonce(self):
        """Create a random verifiable nonce value."""

        salt = "".join(random.choices(self.HEX_DIGITS, k=self.SALT_LENGTH))

        signature = jwt.encode(
            {"exp": datetime.utcnow() + self.NONCE_EXPIRATION, "salt": salt},
            self._secret,
            algorithm="HS256",
        )

        return signature

    def _check_nonce(self, nonce):
        """Check a nonce was created with `_get_nonce`.

        :param nonce: String to check
        :return: Boolean indicating if this is a valid nonce
        """
        try:
            jwt.decode(nonce, self._secret, algorithms=["HS256"])
        except InvalidTokenError:
            return False

        return True

    def login_url(self, login_hint=None, force_login=False, next_=None):
        """Generate URL for request to Google's OAuth 2.0 server.

        :param login_hint: Pre-fill the form with this email address
        :param force_login: Force a user to login again, even if Google has a
            cookie for them.
        :param next_: URL to redirect the user after a successful login.
        :raise BadOAuth2Config: If our OAuth2 config is incorrect
        :return: A URL to redirect the user to for login
        """

        authorization_url, state = self._get_flow().authorization_url(
            # Enable offline access so that you can refresh an access token
            # without re-prompting the user for permission. Recommended for
            # web server apps.
            access_type="offline",
            # Enable incremental authorization. Recommended as a best practice.
            include_granted_scopes="true",
            # If we happen to know who is logging in, we can pre-fill the form
            login_hint=login_hint,
            # String value that your application uses to maintain state between
            # your authorization request and the authorization server's response
            state=self._encode_state(
                {
                    "next": next_,
                    # Enable a nonce value we can verify to prevent XSS attacks
                    "nonce": self._get_nonce(),
                }
            ),
            # Should we make the user fill out the form again?
            prompt="select_account" if force_login else None,
        )

        # I'm not sure if we need to check the state coming back from Google,
        # as I think it's just an echo of what we sent, but lets do it anyway
        # as it's quick
        self._assert_state_valid(state)

        return authorization_url

    def exchange_auth_code(self, redirect_url):
        """Handle a callback from Google and get user credentials.

        :param redirect_url: The URL that we received the callback on
        :raise UserNotAuthenticated: If the user fails authentication
        :raise BadOAuth2Config: If our OAuth2 config is incorrect
        :return: A tuple of dicts (user_info, credentials, state)
        """
        query = dict(parse_qsl(urlparse(redirect_url)[4]))

        self._assert_no_errors(query.get("error"))
        self._assert_state_valid(query.get("state"))

        flow = self._get_flow()
        try:
            flow.fetch_token(authorization_response=redirect_url)

        except InvalidGrantError as err:
            raise UserNotAuthenticated(
                "User is not authenticated: token exchange failed"
            ) from err

        except InvalidClientError as err:
            raise BadOAuth2Config("Bad client or secret") from err

        credentials = flow.credentials

        return (
            self._decode_token(credentials.id_token),
            {
                "token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "id_token": credentials.id_token,
                "token_uri": credentials.token_uri,
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "scopes": credentials.scopes,
            },
            self._decode_state(query["state"]),
        )

    def _assert_no_errors(self, error):
        if error:
            raise UserNotAuthenticated(f"Error returned from authentication: {error}")

    def _assert_state_valid(self, state):
        state = self._decode_state(state)
        if not self._check_nonce(state.get("nonce")):
            raise UserNotAuthenticated("State check failed")

    @classmethod
    def _decode_token(cls, id_token):
        """Decode a JWT from Google and verify it."""

        # https://developers.google.com/identity/protocols/oauth2/openid-connect#validatinganidtoken
        try:
            # Don't bother checking this came from Google, we know the request
            # came from Google by virtue of the state/nonce.
            return jwt.decode(id_token, options={"verify_signature": False})

        except InvalidTokenError as err:
            # This could actually be because we have the wrong key... but we
            # can't tell the difference, and this is more likely
            raise UserNotAuthenticated(
                "Invalid JWT token: cannot determine user details"
            ) from err

    def _get_flow(self):
        """Get a Google OAuth Flow object."""

        # The google examples show passing "project_id" and "redirect_urls",
        # but they appear to have no effect
        client_args = {
            # Dynamic things
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            # Static things
            "auth_uri": self.OPEN_ID_DISCOVERY["authorization_endpoint"],
            "token_uri": self.OPEN_ID_DISCOVERY["token_endpoint"],
        }

        try:
            flow = Flow.from_client_config({"web": client_args}, scopes=self.SCOPES)
        except ValueError as err:
            raise BadOAuth2Config("The authentication config is invalid") from err

        # Indicate where the API server will redirect the user. This must match
        # our pre-registered redirect URIs.
        flow.redirect_uri = self._redirect_uri

        return flow


def factory(_context, request):
    return GoogleAuthService(
        secret=request.registry.settings["pyramid_googleauth.secret"],
        client_config={
            # The client id and secret are provided by Google and are different
            # from env to env. So we read these from environment variables in
            # `app.py`
            "client_id": request.registry.settings[
                "pyramid_googleauth.google_client_id"
            ],
            "client_secret": request.registry.settings[
                "pyramid_googleauth.google_client_secret"
            ],
            # Until this route exists we'll use a hard coded value
            "redirect_uri": request.route_url("pyramid_googleauth.login.callback"),
        },
    )
