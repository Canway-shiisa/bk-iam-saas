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
# Generated by Django 2.2.10 on 2020-05-20 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('group', '0003_auto_20200401_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='creator',
            field=models.CharField(max_length=64, verbose_name='创建者'),
        ),
        migrations.AlterField(
            model_name='group',
            name='updater',
            field=models.CharField(max_length=64, verbose_name='更新者'),
        ),
    ]
