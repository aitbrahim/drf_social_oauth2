# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-06 18:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import social_oauth2.fields
import social_oauth2.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSocialAuth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('provider', models.CharField(max_length=32)),
                ('uid', models.CharField(max_length=255)),
                ('extra_data', social_oauth2.fields.JSONField(default=dict)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='social_auth', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'social_auth_usersocialauth',
            },
            bases=(models.Model, social_oauth2.storage.DjangoUserMixin),
        ),
        migrations.AlterUniqueTogether(
            name='usersocialauth',
            unique_together=set([('provider', 'uid')]),
        ),
    ]
