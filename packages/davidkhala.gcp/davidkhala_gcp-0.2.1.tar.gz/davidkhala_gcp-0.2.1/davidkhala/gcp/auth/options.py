import google.auth
from google.api_core.client_options import ClientOptions as GCPClientOptions
from google.auth.credentials import Credentials
from google.oauth2 import service_account

from davidkhala.gcp.auth import OptionsInterface, ServiceAccountInfo


class ServiceAccount(OptionsInterface):
    credentials: service_account.Credentials


class ADC(OptionsInterface):
    credentials: Credentials


default_scopes = ['googleapis.com/auth/cloud-platform']
"""
[Oauth 2.0 Scopes](https://developers.google.com/identity/protocols/oauth2/scopes)
"""


def default(scopes=None) -> ADC:
    c = ADC()
    c.credentials, c.projectId = google.auth.default(
        scopes=scopes,  # used to get Bearer Token, see in
        default_scopes=default_scopes,
    )
    return c


def from_service_account(info: ServiceAccountInfo = None, *,
                         client_email=None, private_key=None, project_id=None, scopes=None
                         ) -> ServiceAccount:
    if scopes is None:
        scopes = default_scopes
    scopes = list(map(lambda scope: 'https://www.' + scope, scopes))
    if not info:
        info = {
            'client_email': client_email,
            'private_key': private_key,
        }
    if project_id:
        info['project_id'] = project_id

    if not info.get('project_id'):
        info['project_id'] = info.get('client_email').split('@')[1].split('.')[0]

    info['token_uri'] = "https://oauth2.googleapis.com/token"
    c = ServiceAccount()

    c.credentials = service_account.Credentials.from_service_account_info(
        info, scopes=scopes
    )
    c.projectId = info['project_id']
    return c


def from_api_key(api_key: str, client_options: GCPClientOptions = None) -> GCPClientOptions:
    if client_options is None:
        client_options = GCPClientOptions()
    client_options.api_key = api_key
    return client_options
