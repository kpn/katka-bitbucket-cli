from typing import Callable

from django.contrib.auth.models import Group, User

import pytest
from bitbucket.models import KatkaProject
from guardian.shortcuts import assign_perm


@pytest.fixture
def add_user_group_permissions() -> Callable[[str], None]:
    def load_fixture(username: str, project_id: str, group_name: str) -> None:
        user = User.objects.get(username=username)
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        katka_project = KatkaProject.objects.get(project_id=project_id)
        assign_perm('view_katkaproject', group, katka_project)

    return load_fixture
