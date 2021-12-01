# {
#                 "id": "bk_cmdb",
#                 "name": "配置平台",
#                 "policy_info": [
#                     {
#                         "id": "package_version_create",
#                         "related_resource_types": [],
#                         "policy_id": 1408,
#                         "expired_at": 1651990820,
#                         "type": "create",
#                         "name": "程序包版本新建",
#                         "description": "",
#                         "expired_display": "163 天"
#                     },
#                     {
#                         "id": "periodic_task_edit",
#                         "related_resource_types": [
#                             {
#                                 "system_id": "bk_sops",
#                                 "type": "periodic_task",
#                                 "condition": [
#                                     {
#                                         "instances": [
#                                             {
#                                                 "type": "periodic_task",
#                                                 "path": [
#                                                     [
#                                                         {
#                                                             "id": "2",
#                                                             "name": "研发中心",
#                                                             "system_id": "bk_sops",
#                                                             "type": "project",
#                                                             "type_name": "项目"
#                                                         },
#                                                         {
#                                                             "id": "1",
#                                                             "name": "跨业务流程测试_20211012091248",
#                                                             "system_id": "bk_sops",
#                                                             "type": "periodic_task",
#                                                             "type_name": "周期任务"
#                                                         }
#                                                     ],
#                                                     [
#                                                         {
#                                                             "id": "1",
#                                                             "name": "蓝鲸",
#                                                             "system_id": "bk_sops",
#                                                             "type": "project",
#                                                             "type_name": "项目"
#                                                         },
#                                                         {
#                                                             "id": "2",
#                                                             "name": "跨业务子流程定时器_20211012092751",
#                                                             "system_id": "bk_sops",
#                                                             "type": "periodic_task",
#                                                             "type_name": "周期任务"
#                                                         }
#                                                     ],
#                                                     [
#                                                         {
#                                                             "id": "3",
#                                                             "name": "hpux",
#                                                             "system_id": "bk_sops",
#                                                             "type": "project",
#                                                             "type_name": "项目"
#                                                         },
#                                                         {
#                                                             "id": "8",
#                                                             "name": "测试echo",
#                                                             "system_id": "bk_sops",
#                                                             "type": "periodic_task",
#                                                             "type_name": "周期任务"
#                                                         }
#                                                     ]
#                                                 ],
#                                                 "name": "周期任务"
#                                             }
#                                         ],
#                                         "attributes": [],
#                                         "id": "b587830aded34fa7a9aaf54e37560d2f"
#                                     }
#                                 ],
#                                 "name": "周期任务",
#                                 "selection_mode": "instance"
#                             }
#                         ],
#                         "policy_id": 1327,
#                         "expired_at": 4102444800,
#                         "type": "edit",
#                         "name": "周期任务编辑",
#                         "description": "",
#                         "expired_display": "永久"
#                     }
#                 ]
#             }