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
from drf_yasg.utils import swagger_auto_schema
from rest_framework.viewsets import GenericViewSet

from backend.common.swagger import ResponseSwaggerAutoSchema
from rest_framework import status, views
from drf_yasg.openapi import Response as yasg_response

from backend.apps.handover.models import HandOverRecord, HandOverTaskDetail
from .constants import HandoverStatus
from .tasks import handover_task


handover_logger = logging.getLogger("handover")


class HandOverViewSet(GenericViewSet):

    paginator = None  # 去掉swagger中的limit offset参数

    @swagger_auto_schema(
        operation_description="执行权限交接",
        auto_schema=ResponseSwaggerAutoSchema,
        responses={status.HTTP_200_OK: yasg_response({})},
        tags=["handover"],
    )
    def create(self, request, *args, **kwargs):
        pass

    def get(self, request, *args, **kwargs):

        handover_data = request.data
        executor = request.user.username
        transferor = handover_data["transferor"]
        reason = handover_data["reason"]
        handover_info = handover_data["handover_info"]



        # print(handover_data)

        try:
            # check()  # 加锁，避免同一个任务重复执行：

            handover_record = HandOverRecord.objects.create(executor=executor,
                                                            transferor=transferor,
                                                            reason=reason)
            record_id = handover_record.id
            print(record_id, "recccccccccc")
        except...:
            handover_logger.exception("")
            handover_record = HandOverRecord.objects.create(executor=executor,
                                                            transferor=transferor,
                                                            status=HandoverStatus.Failed.value,
                                                            reason=reason)
            record_id = handover_record.id
            return Response({"id": record_id})

        # 批量创建交接明细记录
        handover_task_details = []
        for category in handover_info:
            for obj in handover_info[category]:

                handover_task_details.append(
                    HandOverTaskDetail(
                        handover_record_id=record_id,
                        object_type=category,
                        object_id=obj["id"],
                        object_detail=obj,
                        error_info=""
                    )
                )
        if not handover_task_details:
            return
        HandOverTaskDetail.objects.bulk_create(handover_task_details)

        # return Response({})

        # 异步执行任务
        # handover_task.delay(executor=handover_record.executor, transferor=handover_record.transferor, record_id=record_id)
        handover_task(executor=executor, transferor=transferor, record_id=record_id)

        # # 全部执行完毕，通过HandOverTaskDetail表所有子任务的状态来判断是成功还是部分成功
        # task_status = set(HandOverTaskDetail.objects.filter(handover_task_id=record_id).values_list("status", flat=True))
        # if "Faild" in task_status and "Success" in task_status:
        #     HandOverRecord.objects.filter(id=record_id).update(status="Partial Success")  # 更新任务记录
        # elif "Faild" in task_status and "Success" not in task_status:
        #     HandOverRecord.objects.filter(id=record_id).update(status="Faild")  # 更新任务记录
        # elif "Faild" not in task_status and "Success" in task_status:
        #     HandOverRecord.objects.filter(id=record_id).update(status="Success")  # 更新任务记录
        #
        return Response({"id": record_id})


class HandOverRecordsViewSet(GenericViewSet):
    def list(self):
        pass
    def retrieve(self):
        pass


