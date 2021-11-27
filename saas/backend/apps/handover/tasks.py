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
import logging
from celery import task
from rest_framework.response import Response

from backend.apps.handover.models import HandOverTaskDetail
from .utils import (
    GroupHandover, CustomHandover, SystemManHandler, SuperManHandler, RatingManHandler)

execute_handover_map = {
    "group": GroupHandover,
    "custom": CustomHandover,
    "super_man": SuperManHandler,
    "system_man": SystemManHandler,
    "rating_man": RatingManHandler
}


@task(ignore_result=True)
def handover_task(executor, transferor, record_id):
    # 获取子任务列表
    task_list = HandOverTaskDetail.objects.filter(handover_task_id=record_id)

    # 循环执行子任务
    for task in task_list:
        task_info = task.to_dict()

    # 根据任务类别获取对应执行的类方法，每个子任务执行的成功或失败不相干扰
        try:
            handover_handler = execute_handover_map[task_info["object_type"]]()
            # 交接处理
            handover_handler.handler(executor, transferor, task_info)
            HandOverTaskDetail.objects.filter(handover_task_id=task_info.id).update(status="Success")  # 权限交接详情表记录

            return Response({})
        except:
            HandOverTaskDetail.objects.filter(handover_task_id=task_info.id).update(status="Faild")  # 权限交接详情表记录

