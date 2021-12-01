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
from aenum import StrEnum, auto, skip
from django.utils.translation import gettext as _

from backend.util.enum import ChoicesEnum
from backend.biz.handover import GroupHandover, CustomHandover, SuperManHandler, SystemManHandler, RatingManHandler


execute_handover_map = {
    "group": GroupHandover,
    "custom": CustomHandover,
    "super_man": SuperManHandler,
    "system_man": SystemManHandler,
    "rating_man": RatingManHandler
}


class HandoverStatus(ChoicesEnum, StrEnum):
    """权限交接的执行状态"""

    Running = auto()
    Succeed = auto()
    Failed = auto()
    PartialSucceed = auto()

    _choices_labels = skip(((Running, _("正在交接")), (Succeed, _("交接成功")), (Failed, _("交接失败")), (PartialSucceed, _("部分成功"))))


class HandoverTaskStatus(ChoicesEnum, StrEnum):
    """权限交接具体任务的执行状态"""

    Running = auto()
    Succeed = auto()
    Failed = auto()

    _choices_labels = skip(((Running, _("正在交接")), (Succeed, _("交接成功")), (Failed, _("交接失败"),)))


class HandoverObjectType(ChoicesEnum, StrEnum):
    """交接的权限类型"""

    group = auto()
    custom = auto()
    super_manager = auto()
    system_manager = auto()
    rating_manager = auto()

    _choices_labels = skip(((group, _("用户组权限")), (custom, _("自定义权限")), (super_manager, _("超级管理员权限")),
                            (system_manager, _("系统管理员权限")), (rating_manager, _("分级管理员权限"))))
