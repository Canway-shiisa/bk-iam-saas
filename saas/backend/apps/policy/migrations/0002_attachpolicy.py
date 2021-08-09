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
# Generated by Django 2.2.10 on 2020-03-05 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('policy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachPolicy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creator', models.CharField(max_length=32, verbose_name='创建者')),
                ('updater', models.CharField(max_length=32, verbose_name='更新者')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('subject_type', models.CharField(max_length=32)),
                ('subject_id', models.CharField(max_length=32)),
                ('system_id', models.CharField(max_length=32)),
                ('action_type', models.CharField(max_length=32, verbose_name='操作类型')),
                ('action_id', models.CharField(max_length=64, verbose_name='操作ID')),
                ('policy_id', models.BigIntegerField(default=0, verbose_name='后端policy_id')),
            ],
            options={
                'verbose_name': '附加策略',
                'verbose_name_plural': '附加策略',
            },
        ),
    ]
