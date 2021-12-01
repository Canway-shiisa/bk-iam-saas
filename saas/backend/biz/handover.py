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
from backend.biz.group import GroupBiz
from backend.biz.policy import PolicyOperationBiz, PolicyBean
from backend.biz.role import RoleBiz
from backend.service.models import Subject
from backend.service.constants import SubjectType

# 加锁，避免同一个任务重复执行：
def check():
    pass

# 判断用户权限归属与是否过期：
def verify_permission(permission_info):
    # if role_id != 0 and not RoleUser.objects.user_role_exists(request.user.username, role_id):
    #     raise error_codes.FORBIDDEN.format(_("您没有该角色权限，无法切换到该角色"), True)
    pass


def verify_group_permission(subject, group_id):
    subject_groups = GroupBiz().list_subject_group(subject=subject)
    for subject_group in subject_groups:
        if subject_group.id == group_id and subject_group.expired_at != 0:
            return True
    return False


def verify_custom_permission(subject, group_id):
    pass

def verify_role_permission():
    pass

# 用户组授权类
class GroupHandover:
    def handler(self, executor, transferor, object_detail):
        grant_subject = Subject(**{"type": SubjectType.USER.value, "id": transferor})
        remove_subject = Subject(**{"type": SubjectType.USER.value, "id": executor})
        expired_at = object_detail["expired_at"]
        group_id = object_detail["id"]

        vertify_flag = verify_group_permission(subject=remove_subject, group_id=group_id)  # 判断用户权限归属与是否过期
        if vertify_flag:
            # GroupCheckBiz().check_member_count(group_id, len(grant_subject))    # 检查用户组成员数量未超限
            # GroupCheckBiz().check_subject_group_limit()   # 检查subject授权的group数量是否超限

            # 用户组增加成员
            GroupBiz().add_members(group_id, [grant_subject], expired_at)
            # 用户组移除成员
            # GroupBiz().remove_members(group_id, [remove_subject])


class CustomHandover:
    def handler(self, executor, transferor, object_detail):
        # vertify_flag = verify_custom_permission()  # 判断用户权限归属与是否过期


        vertify_flag = True
        if vertify_flag:
            system_id = object_detail["id"]
            grant_subject = Subject(type=SubjectType.USER.value, id=transferor)
            remove_subject = Subject(type=SubjectType.USER.value, id=executor)
            policy_info = object_detail["policy_info"]
            policies = []
            for policy in policy_info:
                policies.append(PolicyBean(**policy))


            # 授权
            PolicyOperationBiz().alter(system_id=system_id, subject=grant_subject, policies=policies)

            # 移除权限
            # remove_subject = Subject(type=SubjectType.USER.value, id=executor)
            PolicyOperationBiz.revoke(system_id=system_id, subject=remove_subject, policies=policies)


class SuperManHandler:
    def handler(self, executor, transferor, task_info):
        vertify_flag = verify_permission(task_info)  # 判断用户权限归属与是否过期
        if vertify_flag:
            # 授权
            # system_permission_enabled = p判断用户是否拥有系统的所有权限，其实是否只需要上一步中判断是否为超级管理员就可以了，是的话就直接可以交接出去？
            RoleBiz().add_super_manager_member(transferor, True)    # 将被交接人添加为超级管理员角色
            # 移除权限
            RoleBiz().delete_super_manager_member(executor)  # 删除交接人的超级管理员角色


class SystemManHandler:
    def handler(self, executor, transferor, task_info):
        vertify_flag = verify_permission(task_info)  # 判断用户权限归属与是否过期
        if vertify_flag:
            # 修改系统管理员成员,这里的成员列表可能要重新获取一下?
            members = task_info["object_detail"]["members"]

            members.append(transferor)  # 将被交接人添加到系统管理员成员列表
            members.remove(executor)    # 将交接人从系统管理员列表中移除
            RoleBiz().modify_system_manager_members(task_info["object_id"], members)
            # 授权
            # biz.role.RoleBiz.add_system_manager_members()  # 修改系统管理员
            # 移除权限
            # biz.role.RoleBiz.delete_member()  # 角色删除成员


class RatingManHandler:
    def handler(self, executor, transferor, task_info):
        vertify_flag = verify_permission(task_info)  # 判断用户权限归属与是否过期

        if vertify_flag:
            # 授权
            role_id = task_info["object_detail"]["policy_info"]["id"]
            grant_members = list(transferor)
            RoleBiz().add_grade_manager_members(role_id, grant_members)  # 将交接人添加为分级管理员成员
            # 移除权限
            RoleBiz().delete_member(role_id, executor)  # 角色删除成员



