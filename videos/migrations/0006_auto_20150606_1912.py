# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0005_auto_20150606_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='slug',
            field=models.SlugField(null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='video',
            unique_together=set([('slug', 'category')]),
        ),
    ]
