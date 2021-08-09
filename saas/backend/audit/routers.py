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
from backend.audit.apps import AuditConfig
from backend.audit.models import get_audit_db


class AuditRouter:
    """
    A router to control all database operations on models in the
    audit application.
    """

    app_label = AuditConfig.name

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to audit.
        """
        if model._meta.app_label == self.app_label:
            return get_audit_db()
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to audit.
        """
        if model._meta.app_label == self.app_label:
            return get_audit_db()
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the audit app is involved.
        """
        if obj1._meta.app_label == self.app_label or obj2._meta.app_label == self.app_label:
            return False
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'audit'
        database.
        """
        if app_label == self.app_label:
            return False
        return None
