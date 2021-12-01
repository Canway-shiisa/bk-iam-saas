# Generated by Django 2.2.24 on 2021-12-01 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='HandOverRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('executor', models.CharField(max_length=64, verbose_name='交接人')),
                ('transferor', models.CharField(max_length=64, verbose_name='被交接人')),
                ('status', models.CharField(choices=[('Running', '正在交接'), ('Succeed', '交接成功'), ('Failed', '交接失败'), ('PartialSucceed', '部分成功')], default='Running', max_length=16, verbose_name='交接状态')),
                ('reason', models.CharField(max_length=255, verbose_name='交接原因')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HandOverTaskDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_time', models.DateTimeField(auto_now=True)),
                ('handover_record_id', models.IntegerField(verbose_name='交接任务id')),
                ('object_type', models.CharField(choices=[('group', '用户组权限'), ('custom', '自定义权限'), ('super_manager', '超级管理员权限'), ('system_manager', '系统管理员权限'), ('rating_manager', '分级管理员权限')], max_length=16, verbose_name='权限类别')),
                ('object_id', models.IntegerField(verbose_name='权限ID')),
                ('object_detail', models.TextField(verbose_name='所交接权限的详情')),
                ('status', models.CharField(choices=[('Running', '正在交接'), ('Succeed', '交接成功'), ('Failed', '交接失败')], default='Running', max_length=16, verbose_name='交接状态')),
                ('error_info', models.TextField(verbose_name='交接异常信息')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
