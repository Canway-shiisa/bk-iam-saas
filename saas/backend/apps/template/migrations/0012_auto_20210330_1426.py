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
# Generated by Django 2.2.14 on 2021-03-30 06:26

from django.db import migrations

import backend.common.models


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0011_permtemplatepregroupsync_permtemplatepreupdatelock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permtemplatepregroupsync',
            name='_data',
        ),
        migrations.RemoveField(
            model_name='permtemplatepreupdatelock',
            name='_action_ids',
        ),
        migrations.AddField(
            model_name='permtemplatepregroupsync',
            name='data',
            field=backend.common.models.CompressedJSONField(default=None, verbose_name='授权数据'),
        ),
        migrations.AddField(
            model_name='permtemplatepreupdatelock',
            name='action_ids',
            field=backend.common.models.CompressedJSONField(default=None, verbose_name='操作列表'),
        ),
    ]
