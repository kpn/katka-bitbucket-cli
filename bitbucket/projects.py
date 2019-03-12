import logging
from dataclasses import dataclass

from .service import BitbucketService

log = logging.getLogger(__name__)


@dataclass
class BitbucketProjects(BitbucketService):
    filter_name: str = None
    permission: str = None

    SERVICE_KEY_MAP = BitbucketService.SERVICE_KEY_MAP + (
        ('filter_name', 'name'),
        ('permission', 'permission')
    )

    def get_projects(self, params: dict = None) -> dict:
        params = params or {}

        return self.get(path='projects', params=params)
