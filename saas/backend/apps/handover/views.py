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
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from backend.apps.handover.models import HandOverRecord, HandOverTaskDetail
import json
from .tasks import handover_task


handover_logger = logging.getLogger("handover")


class HandOverViewSet(GenericViewSet):
    def create(self, request, *args, **kwargs):
        handover_data = json.loads(request.data)

        try:
            # check()  # 加锁，避免同一个任务重复执行：

            handover_record = HandOverRecord.objects.create(executor=request.user.username,
                                                            transferor=handover_data["transferor"],
                                                            status="RUNNING",
                                                            reason=handover_data["reason"])  # 创建任务记录
            record_id = handover_record.id

        except:
            handover_logger.exception("")
            handover_record = HandOverRecord.objects.create(executor=request.user.username,
                                                            transferor=handover_data["transferor"],
                                                            status="Failed",
                                                            reason=handover_data["reason"])  # 创建任务记录
            return handover_record.id

    # 批量创建交接细节记录
        for category in handover_data["handover_info"]:
            handover_details = [
                HandOverTaskDetail(
                    handover_task_id=record_id,
                    object_category=category,
                    status="Running",
                    object_id=obj["id"]
                )
                for obj in handover_data["handover_info"][category]
            ]
            HandOverTaskDetail.objects.bulk_create(handover_details)

        # 异步执行任务
        handover_task.delay(executor=handover_record.executor, transferor=handover_record.transferor, record_id=record_id)

        # 全部执行完毕，通过HandOverTaskDetail表所有子任务的状态来判断是成功还是部分成功
        task_status = set(HandOverTaskDetail.objects.filter(handover_task_id=record_id).values_list("status", flat=True))
        if "Faild" in task_status and "Success" in task_status:
            HandOverRecord.objects.filter(id=record_id).update(status="Partial Success")  # 更新任务记录
        elif "Faild" in task_status and "Success" not in task_status:
            HandOverRecord.objects.filter(id=record_id).update(status="Faild")  # 更新任务记录
        elif "Faild" not in task_status and "Success" in task_status:
            HandOverRecord.objects.filter(id=record_id).update(status="Success")  # 更新任务记录

        return Response({"data": record_id})


