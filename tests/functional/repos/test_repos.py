from django.contrib.auth.models import Group, User
from django.urls import reverse

import mock
import pytest
from bitbucket.models import KatkaProject
from guardian.shortcuts import assign_perm
from requests import HTTPError, Response

from ..mixins import AuthNAuthZMixin


@pytest.mark.django_db(transaction=True)
@pytest.mark.usefixtures('load_db_fixture')
@pytest.mark.parametrize(
    'load_db_fixture', [{'fixture_filename': 'katka_project.json'}], indirect=True)
@mock.patch('requests.sessions.Session.request')
class TestGetRepos(AuthNAuthZMixin):
    viewname = 'repos'

    def test_existing_repos(self, mock_request, load_db_fixture, add_user_group_permissions, load_json_fixture,
                            client):
        # prepare user
        add_user_group_permissions(username=self.default_username, project_id='4cb432f5-0def-48b6-ad05-f1c082b1f1b8',
                                   group_name='d-nitro')
        client.login(username=self.default_username, password=self.default_password)

        # prepare mocks
        response = mock.Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = load_json_fixture('bitbucket_repos.json')
        mock_request.return_value = response

        endpoint = reverse(self.viewname, kwargs=self.default_view_kwargs)
        response = client.get(
            endpoint,
            content_type='application/json',
            data=self.default_data
        )

        assert response.status_code == 200
        assert len(response.data) == 2
        assert response.data[0]['slug'] == response.data[0]['name'] == 'invisible_women'
        assert response.data[1]['slug'] == response.data[1]['name'] == 'katana'

    def test_empty_project(self, mock_request, load_db_fixture, add_user_group_permissions, load_json_fixture, client):
        # prepare user
        add_user_group_permissions(username=self.default_username, project_id='4cb432f5-0def-48b6-ad05-f1c082b1f1b8',
                                   group_name='d-nitro')
        client.login(username=self.default_username, password=self.default_password)

        # prepare mocks
        response = mock.Mock()
        response.raise_for_status.return_value = None
        response.json.return_value = load_json_fixture('bitbucket_empty_project.json')
        mock_request.return_value = response

        endpoint = reverse(self.viewname, kwargs=self.default_view_kwargs)
        response = client.get(
            endpoint,
            content_type='application/json',
            data=self.default_data
        )

        assert response.status_code == 404
        assert str(response.data['detail']) == 'No repos found for that project_id.'

    def test_katka_project_not_found(self, load_db_fixture, client):
        user = User.objects.get(username=self.default_username)
        group = Group.objects.get(name=self.default_groupname)
        user.groups.add(group)
        katka_project = KatkaProject.objects.get(project_id=self.default_katka_project_id)
        assign_perm('delete_katkaproject', group, katka_project)

        client.login(username=self.default_username, password=self.default_password)

        endpoint = reverse(self.viewname, kwargs=self.default_view_kwargs)
        response = client.get(
            endpoint,
            content_type='application/json',
            data={'katka_project_id': '4cb432f5-0def-48b6-ad05-f1c082b1f1b7', 'limit': 10, 'start': 2}
        )

        assert response.status_code == 404
        assert str(response.data['detail']) == 'Katka project not found.'

    def test_group_not_permitted(self, load_db_fixture, client):
        user = User.objects.get(username=self.default_username)
        group = Group.objects.get(name=self.default_groupname)
        user.groups.add(group)
        katka_project = KatkaProject.objects.get(project_id=self.default_katka_project_id)
        assign_perm('delete_katkaproject', group, katka_project)

        client.login(username=self.default_username, password=self.default_password)

        endpoint = reverse(self.viewname, kwargs=self.default_view_kwargs)
        response = client.get(
            endpoint,
            content_type='application/json',
            data=self.default_data
        )

        assert response.status_code == 403
        assert str(response.data['detail']) == 'You do not have permission to perform this action.'

    def test_unknown_service_exception(self, mock_request, load_db_fixture, add_user_group_permissions,
                                       load_json_fixture, client):
        # prepare user
        add_user_group_permissions(username=self.default_username, project_id='4cb432f5-0def-48b6-ad05-f1c082b1f1b8',
                                   group_name='d-nitro')
        client.login(username=self.default_username, password=self.default_password)

        # prepare mocks
        service_response = Response()
        service_response.status_code = 503
        service_response._content = None
        response = mock.Mock()
        response.raise_for_status.side_effect = HTTPError(response=service_response)
        mock_request.return_value = response

        endpoint = reverse(self.viewname, kwargs=self.default_view_kwargs)
        response = client.get(
            endpoint,
            content_type='application/json',
            data=self.default_data
        )

        assert response.status_code == 500
        assert str(response.data['detail']) == 'A server error occurred.'
