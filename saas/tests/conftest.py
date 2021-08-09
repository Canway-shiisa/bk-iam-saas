# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making 蓝鲸智云-权限中心(BlueKing-IAM) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
# import importlib
# from unittest import mock

import pytest
from django_dynamic_fixture import G
from rest_framework.test import APIClient as DRFAPIClient
from rest_framework.test import ForceAuthClientHandler

from backend.apps.role.models import RoleScope
from backend.service.constants import RoleScopeType, RoleType
from backend.util.json import json_dumps
from tests.test_util.auth import create_auth_role, create_user
from tests.test_util.helpers import generate_random_number
from tests.test_util.init_db import init_role

# def _mock_role_0008_migration():
#     # 由于Role的0008_auto_20201230_1653 Migration调用到第三方，需要Mock，否则Migrate将失败
#     with mock.patch("backend.apps.role.init_data.add_admin_to_super_manager_member") as mocked_method:
#         mocked_method.return_value = None
#         yield
#
#
# def _mock_organization_0004_migration():
#     # Organization的0004_auto_20201230_1653 Migration调用到第三方，需要Mock，否则Migrate将失败
#     with mock.patch("backend.apps.organization.init_data.sync_admin_user") as mocked_method:
#         mocked_method.return_value = None
#         yield
#
#
# mock_role_0008_migration = pytest.fixture(_mock_role_0008_migration, scope="session")
# mock_organization_0004_migration = pytest.fixture(_mock_organization_0004_migration, scope="session")
#
#
# @pytest.fixture(scope="session")
# def django_db_use_migrations(mock_role_0008_migration, mock_organization_0004_migration):
#     """
#     功能：仅仅只是为了触发mock_xxx_migration生效
#     该函数是重载了pytest.fixtures.django_db_use_migrations函数
#     因为在django_db_setup里的执行DB Migrate是由setup_databases触发的
#     所以只能选择django_db_setup在setup_databases调用前的fixture
#     进行重载才能在Migrate之前使Mock生效
#     https://pytest-django.readthedocs.io/en/latest/database.html#django-db-use-migrations
#     """
#     return True


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):
    """Create initial data before test starts, doc:
    https://pytest-django.readthedocs.io/en/latest/database.html#populate-the-database-with-initial-test-data
    """
    with django_db_blocker.unblock():
        init_role()


@pytest.fixture
def bk_user(request):
    """Generate a random user"""
    user = create_user()
    return user


class ForceRoleAuthClientHandler(ForceAuthClientHandler):
    """
    A patched version of ClientHandler that can enforce role authentication
    on the outgoing requests.
    """

    def __init__(self, *args, **kwargs):
        self._force_role = None
        super().__init__(*args, **kwargs)

    def get_response(self, request):
        # This is the simplest place we can hook into to patch the
        # request object.
        request._force_role = self._force_role
        return super().get_response(request)


class APIClient(DRFAPIClient):
    _force_role = None

    def __init__(self, enforce_csrf_checks=False, **defaults):
        super().__init__(**defaults)
        self.handler = ForceRoleAuthClientHandler(enforce_csrf_checks)

    def force_role_authenticate(self, role=None):
        """强制添加上角色身份"""
        self.handler._force_role = role


@pytest.fixture
def api_client(request, bk_user):
    """Return an authenticated client"""
    client = APIClient()
    client.force_authenticate(user=bk_user)
    # 不设置角色的话，默认是以普通用户的角色请求
    return client


@pytest.fixture
def api_client_for_super_manager(request, bk_user):
    """Return an authenticated client which auth user is super manager"""
    client = APIClient()
    client.force_authenticate(user=bk_user)
    auth_role = create_auth_role(RoleType.SUPER_MANAGER.value)
    client.force_role_authenticate(auth_role)
    return client


@pytest.fixture
def gen_api_client_for_system_manager():
    """Return an authenticated client which auth user is system manager"""

    def generate(system_id="bk_test"):
        # 生成系统管理员相关DB数据
        role_id = generate_random_number(2, 100)  # 0默认是Staff, 1默认是SuperManager, 所以只能从2开始
        G(
            RoleScope,
            role_id=role_id,
            type=RoleScopeType.AUTHORIZATION.value,
            content=json_dumps([{"system_id": system_id, "actions": [{"id": "*", "related_resource_types": []}]}]),
        )
        G(RoleScope, role_id=role_id, type=RoleScopeType.SUBJECT.value, content=json_dumps([{"type": "*", "id": "*"}]))
        # 创建认证需要的角色（由于认证的角色必须依赖数据库有对应角色，所以需要在之前就生成相关DB数据）
        auth_role = create_auth_role(RoleType.SYSTEM_MANAGER.value, role_id=role_id)
        # 随意用户
        user = create_user()
        # 返回API Client
        client = APIClient()
        client.force_authenticate(user=user)
        client.force_role_authenticate(auth_role)
        return client

    return generate
