import mock
import pytest
from bitbucket.commits import BitbucketCommits
from bitbucket.exceptions import BitbucketBaseAPIException
from bitbucket import constants


class TestBitbucketRepos:
    @mock.patch('bitbucket.service.BitbucketService.get')
    def test_get_commits(self, mock_get_request):
        repos_service = BitbucketCommits(
            credentials_provider=mock.Mock(), project_key='the_wasp', repository_name='winsome',
            since='7c3d7a55b847f234249936c229bd974626b08a99', merges=constants.MERGE_ONLY
        )
        repos_service.get_commits()

        mock_get_request.assert_called_once_with(
            params={'merges': 'only'},
            path='projects/the_wasp/repos/winsome/commits'
        )

    @mock.patch('bitbucket.service.BitbucketService.get')
    def test_get_commits_with_exception(self, mock_get_request):
        mock_get_request.side_effect = BitbucketBaseAPIException
        repos_service = BitbucketCommits(
            credentials_provider=mock.Mock(), project_key='the_wasp', repository_name='winsome',
            since='7c3d7a55b847f234249936c229bd974626b08a99', merges=constants.MERGE_INCLUDE
        )
        with pytest.raises(BitbucketBaseAPIException):
            repos_service.get_commits()

    def test_get_request_params(self):
        bitbucket_service = BitbucketCommits(
            credentials_provider=mock.Mock(), limit=2, start=4, include_counts=False
        )

        assert bitbucket_service._get_request_params(params={'limit': 1}) == {
            'limit': 1,
            'start': 4,
            'includeCounts': False,
        }
