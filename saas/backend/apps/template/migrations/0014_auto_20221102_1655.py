# Generated by Django 2.2.28 on 2022-11-02 08:55

import json

from django.core.paginator import Paginator
from django.db import migrations

from backend.service.constants import AuthTypeEnum
from backend.util.json import json_dumps


def migrate_template_auth_types(apps, schema_editor):
    """刷新用户组模板授权的auth_types"""
    PermTemplatePolicyAuthorized = apps.get_model("template", "PermTemplatePolicyAuthorized")
    qs = PermTemplatePolicyAuthorized.objects.all()
    paginator = Paginator(qs, 100)

    for i in paginator.page_range:
        for auth in paginator.page(i):
            auth_types = json.loads(auth._auth_types)
            if auth_types:
                continue

            data = json.loads(auth._data)
            for action in data["actions"]:
                if "id" in action:
                    action_id = action["id"]
                elif "action_id" in action:
                    action_id = action["action_id"]
                else:
                    continue

                auth_types[action_id] = AuthTypeEnum.ABAC.value

            auth._auth_types = json_dumps(auth_types)
            auth.save(update_fields=["_auth_types"])


class Migration(migrations.Migration):

    dependencies = [
        ("template", "0013_auto_20220606_1208"),
    ]

    operations = [
        migrations.RunPython(migrate_template_auth_types),
    ]