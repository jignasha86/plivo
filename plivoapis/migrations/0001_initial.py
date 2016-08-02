# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('auth_id', models.CharField(max_length=40, blank=True)),
                ('username', models.CharField(max_length=30, blank=True)),
            ],
            options={
                'db_table': 'account',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='PhoneNumber',
            fields=[
                ('id', models.IntegerField(serialize=False, primary_key=True)),
                ('number', models.CharField(max_length=40, blank=True)),
            ],
            options={
                'db_table': 'phone_number',
                'managed': False,
            },
        ),
    ]
