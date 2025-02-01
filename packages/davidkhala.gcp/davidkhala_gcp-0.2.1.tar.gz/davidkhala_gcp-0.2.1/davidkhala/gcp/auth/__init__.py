from dataclasses import dataclass
from datetime import datetime
from typing import TypedDict, NotRequired, Optional

from google.api_core.client_options import ClientOptions
from google.auth.credentials import CredentialsWithQuotaProject, TokenState


@dataclass
class ServiceAccountInfo(TypedDict):
    client_email: str
    private_key: str
    token_uri: NotRequired[str]
    project_id: NotRequired[str]
    client_id: Optional[str] # for Apache Spark pubsub
    private_key_id: Optional[str] # for Apache Spark pubsub


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
