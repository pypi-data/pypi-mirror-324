from datetime import datetime

import google.auth
from google.api_core.client_options import ClientOptions
from google.auth.credentials import Credentials, CredentialsWithQuotaProject, TokenState


class OptionsInterface:
    credentials: CredentialsWithQuotaProject
    """
    raw secret not cached in credentials object. You need cache it by yourself.
    """
    projectId: str
    client_options: ClientOptions

    @property
    def token(self) -> str:
        """
        :return The bearer token that can be used in HTTP headers to make authenticated requests.
        """
        if self.credentials.token_state != TokenState.FRESH:
            from google.auth.transport.requests import Request
            self.credentials.refresh(Request())
        return self.credentials.token

    @property
    def expiry(self) -> datetime:
        return self.credentials.expiry


default_scopes = ['googleapis.com/auth/cloud-platform']
"""
[Oauth 2.0 Scopes](https://developers.google.com/identity/protocols/oauth2/scopes)
"""


class ADC(OptionsInterface):
    credentials: Credentials


def default(scopes=None) -> ADC:
    c = ADC()
    c.credentials, c.projectId = google.auth.default(
        scopes=scopes,  # used to get Bearer Token
        default_scopes=default_scopes,
    )
    return c
