from django.contrib.auth.models import Group, User
from django.urls import reverse


class AuthNAuthZMixin:
    viewname = None  # it has to be defined per subclass
    default_view_kwargs = {'project_id': 'msap'}
    default_username = 'super_saiyan'
    default_password = 'random_pass'
    default_groupname = 'd-nitro'
    default_katka_project_id = '4cb432f5-0def-48b6-ad05-f1c082b1f1b8'
    default_data = {'katka_project_id': default_katka_project_id, 'limit': 10, 'start': 2}

    def test_not_authenticated(self, load_db_fixture, client):
        endpoint = reverse(self.viewname, kwargs=self.default_view_kwargs)
        response = client.get(
            endpoint,
            content_type='application/json'
        )

        assert response.status_code == 403
        assert str(response.data['detail']) == 'Authentication credentials were not provided.'

    def test_unauthorized(self, load_db_fixture, client):
        client.login(username=self.default_username, password=self.default_password)

        endpoint = reverse(self.viewname, kwargs=self.default_view_kwargs)
        response = client.get(
            endpoint,
            content_type='application/json',
            data=self.default_data
        )

        assert response.status_code == 403
        assert str(response.data['detail']) == 'You do not have permission to perform this action.'

    def test_perm_not_assigned(self, load_db_fixture, client):
        user = User.objects.get(username=self.default_username)
        group = Group.objects.get(name=self.default_groupname)
        user.groups.add(group)
        client.login(username=self.default_username, password=self.default_password)

        endpoint = reverse(self.viewname, kwargs=self.default_view_kwargs)
        response = client.get(
            endpoint,
            content_type='application/json',
            data=self.default_data
        )

        assert response.status_code == 403
        assert str(response.data['detail']) == 'You do not have permission to perform this action.'
