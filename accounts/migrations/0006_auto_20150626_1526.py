# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20150625_1944'),
    ]

    operations = [
        migrations.RenameField(
            model_name='myuser',
            old_name='date_created',
            new_name='timestamp',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='date_created',
            new_name='timestamp',
        ),
    ]
