import mock
from bitbucket.repos import BitbucketRepos


class TestBitbucketRepos:
    @mock.patch('bitbucket.service.BitbucketService.get')
    def test_set_api_path(self, mock_get_request):
        repos_service = BitbucketRepos(
            credentials_provider=mock.Mock(), project_key='the_wasp'
        )
        repos_service.get_repos(params={'foo': 'bar'})

        mock_get_request.assert_called_once_with(params={'foo': 'bar'}, path='projects/the_wasp/repos')
