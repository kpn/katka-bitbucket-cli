from django.utils.functional import cached_property

from .base import KatkaService
from .conf import settings
from .exceptions import katka_service_exception_to_api


class CredentialsProvider:
    @cached_property
    def access_token(self):
        raise NotImplementedError('This method should be implemented by the implementation classes')


class KatkaCredentialsService(CredentialsProvider, KatkaService):
    def __init__(self, request, credential_public_id: str = None):
        self.credential_public_id = credential_public_id

        self.base_url = settings.KATKA_SERVICE_LOCATION.rstrip('/')
        self.base_path = 'credentials'
        self.bearer_token = getattr(request, 'auth')

    @cached_property
    def access_token(self) -> str:
        """
        Provides the access token for given `credential_public_id`.

        Returns:
            str: the access token
        """

        if not self.credential_public_id:
            return None

        path = f'{self.base_path}/{self.credential_public_id}/secrets/{settings.CREDENTIALS_ACCESS_TOKEN_KEY}/'
        url = f'{self.base_url}/{path}'

        resp = super().get(url)

        with katka_service_exception_to_api():
            resp.raise_for_status()

        return resp.json().get('value')
