# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_userprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 7, 58, 31, 379810, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='myuser',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 7, 58, 39, 478639, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 7, 58, 56, 258187, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 10, 7, 59, 1, 997047, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
