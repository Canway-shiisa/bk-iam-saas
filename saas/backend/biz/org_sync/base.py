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
from abc import ABCMeta, abstractmethod


class BaseSyncDBService(metaclass=ABCMeta):
    """组织架构从用户管理同步数据到自身DB的抽象基类"""

    @abstractmethod
    def sync_to_db(self):
        """同步SaaS DB 相关变更"""
        pass


class BaseSyncIAMBackendService(metaclass=ABCMeta):
    """组织架构SaaS同步到IAM后台基础抽象类"""

    @abstractmethod
    def sync_to_iam_backend(self):
        """同步IAM后台 相关变更"""
        pass
