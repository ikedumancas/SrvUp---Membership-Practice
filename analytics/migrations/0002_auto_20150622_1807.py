# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pageview',
            name='count',
        ),
        migrations.AddField(
            model_name='pageview',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 22, 10, 7, 38, 831742, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
