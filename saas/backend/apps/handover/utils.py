

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
            # 授权
            # GroupBiz.add_members()
            # 移除权限
            # GroupBiz.remove_members()
            pass


class CustomHandover:
    def handler(self,executor,transferor,task_info):
        vertify_flag = verify_permission(task_info)  # 判断用户权限归属与是否过期
        if vertify_flag:
            # 授权
            # 移除权限
            # PolicyOperationBiz.alter
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


