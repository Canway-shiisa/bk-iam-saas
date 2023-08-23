# Generated by Django 3.2.16 on 2023-08-18 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('role', '0016_auto_20230720_1759'),
    ]

    operations = [
        migrations.AlterField(
            model_name='role',
            name='type',
            field=models.CharField(choices=[('staff', '个人用户'), ('super_manager', '超级管理员'), ('system_manager', '系统管理员'), ('rating_manager', '分级管理员'), ('subset_manager', '子集管理员')], db_index=True, max_length=32, verbose_name='类型'),
        ),
        migrations.AlterField(
            model_name='roleuser',
            name='username',
            field=models.CharField(db_index=True, max_length=64, verbose_name='用户id'),
        ),
        migrations.AlterIndexTogether(
            name='roleuser',
            index_together={('role_id', 'username')},
        ),
    ]