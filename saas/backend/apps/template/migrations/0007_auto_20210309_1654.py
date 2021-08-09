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
# Generated by Django 2.2.14 on 2021-03-09 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0006_auto_20200520_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='permtemplate',
            name='_action_ids',
            field=models.TextField(db_column='action_ids', default='[]', verbose_name='操作列表'),
        ),
        migrations.AddField(
            model_name='permtemplatepolicyauthorized',
            name='_data',
            field=models.TextField(db_column='data', default='{}', verbose_name='授权数据'),
        ),
    ]
