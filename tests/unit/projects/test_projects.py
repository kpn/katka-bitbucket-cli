import mock
from bitbucket.projects import BitbucketProjects


class TestBitbucketProjects:
    def test_get_request_params(self):
        bitbucket_service = BitbucketProjects(
            credentials_provider=mock.Mock(), limit=2, start=4, filter_name='filter_it', permission='READ'
        )

        assert bitbucket_service._get_request_params(params={'limit': 1}) == {
            'name': 'filter_it',
            'limit': 1,
            'start': 4,
            'permission': 'READ'
        }
