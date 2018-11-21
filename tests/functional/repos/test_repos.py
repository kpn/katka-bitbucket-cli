from django.urls import reverse

import mock
import pytest


class TestGetRepos:
    @pytest.mark.django_db(transaction=True)
    @pytest.mark.usefixtures('load_db_fixture')
    @pytest.mark.parametrize(
        'load_db_fixture', [{'fixture_filename': 'katka_project.json'}], indirect=True)
    @mock.patch('requests.sessions.Session.request')
    def test_existing_repos(self, mock_request, load_db_fixture, load_json_fixture, client):
        response = mock.Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = load_json_fixture('bitbucket_repos.json')
        mock_request.return_value = response

        endpoint = reverse('repos', kwargs={'project_id': 'msap'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': '4cb432f5-0def-48b6-ad05-f1c082b1f1b8', 'limit': 10, 'start': 2}
        )

        assert len(response.data) == 2
        assert response.data[0]['slug'] == response.data[0]['name']
        assert response.data[1]['slug'] == response.data[1]['name']

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.usefixtures('load_db_fixture')
    @pytest.mark.parametrize(
        'load_db_fixture', [{'fixture_filename': 'katka_project.json'}], indirect=True)
    @mock.patch('requests.sessions.Session.request')
    def test_empty_project(self, mock_request, load_db_fixture, load_json_fixture, client):
        response = mock.Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = load_json_fixture('bitbucket_empty_project.json')
        mock_request.return_value = response

        endpoint = reverse('repos', kwargs={'project_id': 'msap'})
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': '4cb432f5-0def-48b6-ad05-f1c082b1f1b8', 'limit': 10, 'start': 2}
        )

        assert response.status_code == 404
