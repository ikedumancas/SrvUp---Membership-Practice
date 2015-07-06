# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0012_auto_20150622_1730'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='video',
            options={'ordering': ['order', '-timestamp']},
        ),
        migrations.RenameField(
            model_name='category',
            old_name='date_created',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='video',
            old_name='date_created',
            new_name='timestamp',
        ),
    ]
