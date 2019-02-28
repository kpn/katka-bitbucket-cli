from dataclasses import dataclass

from . import constants
from .service import BitbucketService


@dataclass
class BitbucketCommits(BitbucketService):
    project_key: str = None
    repository_name: str = None
    merges: str = None
    since: str = None
    until: str = None
    include_counts: bool = None

    SERVICE_KEY_MAP = BitbucketService.SERVICE_KEY_MAP + (
        ('merges', 'merges'),
        ('since', 'since'),
        ('until', 'until'),
        ('include_counts', 'includeCounts'),
    )

    def get_commits(self) -> dict:
        path = f'projects/{self.project_key}/repos/{self.repository_name}/commits'

        # translate service specific request params value
        merges = constants.BITBUCKET_MERGES_CONTROL_SERVICE_MAP.get(self.merges) if self.merges else None

        return super().get(path=path, params={'merges': merges})
