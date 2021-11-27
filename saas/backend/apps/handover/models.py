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


class HandOverRecord(TimestampedModel):
    """
    交接任务
    """
    executor = models.CharField("交接人")
    transferor = models.CharField("被交接人")
    status = models.CharField("交接状态")
    reason = models.CharField("交接原因")


class HandOverTaskDetail(TimestampedModel):
    """
    交接任务明细
    """
    handover_task_id = models.IntegerField("交接任务id")
    object_type = models.CharField("权限类别")
    object_id = models.CharField("权限ID")    # 用户组ID/系统ID/角色ID
    object_detail = models.CharField("所交接权限的详情")
    status = models.CharField("交接状态")
    error_info = models.CharField("交接异常信息")
