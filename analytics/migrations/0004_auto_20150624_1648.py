# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0003_auto_20150622_1816'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageview',
            options={'ordering': ['-date_created']},
        ),
    ]
