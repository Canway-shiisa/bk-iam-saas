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
from django.db import models

from backend.common.models import TimestampedModel
from backend.apps.handover.constants import HandoverStatus, HandoverTaskStatus, HandoverObjectType


class HandOverRecord(TimestampedModel):
    """
    交接任务
    """
    executor = models.CharField("交接人", max_length=64)
    transferor = models.CharField("被交接人", max_length=64)
    status = models.CharField(
        "交接状态", choices=HandoverStatus.get_choices(), default=HandoverStatus.Running.value, max_length=16
    )
    reason = models.CharField("交接原因", max_length=255)


class HandOverTaskDetail(TimestampedModel):
    """
    交接任务明细
    """
    handover_record_id = models.IntegerField("交接任务id")
    object_type = models.CharField(
        "权限类别", choices=HandoverObjectType.get_choices(), max_length=16)
    object_id = models.CharField("权限ID", max_length=68)    # 用户组ID/系统ID/角色ID
    object_detail = models.TextField("所交接权限的详情")
    status = models.CharField(
        "交接状态", choices=HandoverTaskStatus.get_choices(), default=HandoverTaskStatus.Running.value, max_length=16
    )
    error_info = models.TextField("交接异常信息")

    def __str__(self):
        # return f"{self.id}-{self.object_type}-{self.object_id}"
        return f"{self.handover_record_id}-{self.object_type}-{self.object_id}"

