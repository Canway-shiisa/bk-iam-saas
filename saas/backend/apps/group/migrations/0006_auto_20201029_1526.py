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
# Generated by Django 2.2.16 on 2020-10-29 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0005_auto_20200813_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='group',
            name='approval_process_id',
        ),
        migrations.RemoveField(
            model_name='group',
            name='approval_process_name',
        ),
    ]
