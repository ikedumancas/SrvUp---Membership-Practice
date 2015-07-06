# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0006_auto_20150606_1912'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='share_message',
            field=models.TextField(default=b'\nCheck out this awesome video.\n'),
        ),
    ]
