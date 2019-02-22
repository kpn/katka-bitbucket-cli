import logging

from dataclasses import dataclass

from .base import KatkaService
from .conf import settings
from .credentials import CredentialsProvider
from .exceptions import bitbucket_service_exception_to_api

log = logging.getLogger(__name__)


@dataclass
class BitbucketService(KatkaService):
    credentials_provider: CredentialsProvider = None
    base_url: str = None

    start: int = None
    limit: int = None

    def __post_init__(self):
        """
        Raises:
            bitbucket.models.KatkaProject.DoesNotExist: in case the given id for the katka project does not exist
        """
        self.base_url = self.base_url or settings.DEFAULT_BITBUCKET_SERVICE_LOCATION
        self.base_url = self.base_url.rstrip('/')
        self.base_path = 'rest/api/1.0'
        self.bearer_token = self.credentials_provider.access_token if self.credentials_provider else None

    def get(self, path: str = '', params: dict = None) -> dict:
        """
        Args:
            path(str): the specific path to get the resource from
            params(dict): the params for query string

        Returns:
            dict: the http response body

        Raises:
            requests.exceptions.HTTPError: in case there is a HTTP error during the request
        """
        url = f'{self.base_url}/{self.base_path}/{path}'
        params = params or {}
        if self.start is not None:
            params['start'] = self.start
        if self.limit is not None:
            params['limit'] = self.limit

        resp = super().get(url, params=params)

        with bitbucket_service_exception_to_api():
            resp.raise_for_status()

        return resp.json()
