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
from .constants import HandoverTaskStatus, execute_handover_map


@task(ignore_result=True)
def handover_task(executor, transferor, record_id):
    # 获取子任务明细列表
    handover_task_details = HandOverTaskDetail.objects.filter(handover_record_id=record_id)

    # 循环执行子任务
    for task_detail in handover_task_details:
        task_detail_id = task_detail.id
        # handover_record_id = task_detail.handover_record_id
        object_type = task_detail.object_type
        object_detail = eval(task_detail.object_detail)

        if object_type == "custom":
    # # 根据任务类别获取对应执行的类方法，每个子任务执行的成功或失败不相干扰
    #         try:
                handover_handler = execute_handover_map[object_type]()
                # 交接处理
                handover_handler.handler(executor, transferor, object_detail)
                HandOverTaskDetail.objects.filter(id=task_detail_id).update(status=HandoverTaskStatus.Succeed.value)
                # return

            # except Exception as e:
            #     HandOverTaskDetail.objects.filter(id=task_detail_id).update(status=HandoverTaskStatus.Failed.value, error_info={e})
                # return


