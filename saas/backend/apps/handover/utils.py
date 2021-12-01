from pydantic.tools import parse_obj_as
from typing import List
from backend.service.models import Subject
from backend.biz.group import GroupBiz, GroupCheckBiz
from backend.service.models import Subject
from backend.service.constants import SubjectRelationType, SubjectType

# 加锁，避免同一个任务重复执行：
def check():
    pass


# 判断用户权限归属与是否过期：
def verify_permission(permission_info):
    pass


# 用户组授权类
class GroupHandover:
    def handler(self, executor, transferor, task_info):
        vertify_flag = verify_permission(task_info)  # 判断用户权限归属与是否过期
        if vertify_flag:
            # 用户组增加成员
            members_data = transferor
            expired_at = task_info["object_detail"]["expired_at"]

            # 成员Dict结构转换为Subject结构，并去重
            members = list(set(parse_obj_as(List[Subject], members_data)))

            # 检查用户组成员数量未超限
            GroupCheckBiz().check_member_count(task_info["object_detail"]["id"], len(members))
            # 添加成员
            GroupBiz().add_members(task_info["object_detail"]["id"], members, expired_at)

            # 用户组移除成员
            subject = Subject(type=SubjectType.USER.value, id=executor)
            GroupBiz().remove_members(task_info["object_detail"]["id"], subject)


class CustomHandover:
    def handler(self, executor, transferor, task_info):
        vertify_flag = verify_permission(task_info)  # 判断用户权限归属与是否过期
        if vertify_flag:
            # 授权
            # 移除权限
            # PolicyOperationBiz.alter(task_info.object_id,)
            pass


class SuperManHandler:
    def handler(self, executor,transferor,task_info):
        vertify_flag = verify_permission(task_info)  # 判断用户权限归属与是否过期
        if vertify_flag:
            # 授权
            # biz.role.RoleBiz.add_super_manager_member()	# 将被交接人添加为超级管理员角色
            # 移除权限
            # biz.role.RoleBiz.delete_super_manager_member()  # 删除交接人的超级管理员角色

            pass



class SystemManHandler:
    def handler(self, executor,transferor,task_info):
        vertify_flag = verify_permission(task_info)  # 判断用户权限归属与是否过期
        if vertify_flag:
            # 授权
            # biz.role.RoleBiz.add_system_manager_members()  # 修改系统管理员
            # 移除权限
            # biz.role.RoleBiz.delete_member()  # 角色删除成员

            pass


class RatingManHandler:
    def handler(self, executor,transferor,task_info):
        vertify_flag = verify_permission(task_info)  # 判断用户权限归属与是否过期
        if vertify_flag:
            # 授权
            # biz.role.RoleBiz.add_grade_manager_members()  # 将交接人添加为分级管理员成员
            # 移除权限
            # biz.role.RoleBiz.delete_member()  # 角色删除成员

            pass


