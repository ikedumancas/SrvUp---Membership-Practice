# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20150626_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='membership',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 26, 6, 57, 29, 68188, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='membership',
            name='date_start',
            field=models.DateTimeField(default=datetime.datetime(2015, 6, 26, 6, 57, 29, 68127, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='success',
            field=models.BooleanField(default=True),
        ),
    ]
