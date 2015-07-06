# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0004_auto_20150624_1648'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageview',
            options={'ordering': ['-timestamp']},
        ),
        migrations.RenameField(
            model_name='pageview',
            old_name='date_created',
            new_name='timestamp',
        ),
    ]
