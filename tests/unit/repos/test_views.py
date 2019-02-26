from django.urls import reverse

import mock
from bitbucket.exceptions import ProjectNotFoundAPIException


class TestGetBitbucketReposView:
    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_get_existing_repos(self, mock_bitbucket_repos, client):
        result = mock.Mock()
        result.get_repos.return_value = {
            'values': [
                {'name': 'super_man', 'slug': 'super'},
                {'name': 'batman', 'slug': 'bat'},
            ]
        }
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_key': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'credential': 'bead677e-c414-4954-85eb-67ef09ca99f7', 'limit': 10, 'start': 2}
        )

        assert response.status_code == 200
        assert len(response.data['values']) == 2

    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_empty_repos_list(self, mock_bitbucket_repos, client):
        result = mock.Mock()
        result.get_repos.return_value = {}
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_key': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'credential': 'bead677e-c414-4954-85eb-67ef09ca99f7'}
        )

        assert response.status_code == 200
        assert len(response.data['values']) == 0
        assert response.data.get('start') is None

    @mock.patch('bitbucket.views.BitbucketRepos')
    def test_bitbucket_project_not_found(self, mock_bitbucket_repos, client):
        result = mock.Mock()
        result.get_repos.side_effect = ProjectNotFoundAPIException
        mock_bitbucket_repos.return_value = result

        endpoint = reverse('repos', kwargs={'project_key': 'TIPD'})
        response = client.get(
            endpoint,
            content_type='application/json'
        )

        assert response.status_code == 404
