# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0009_taggeditem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taggeditem',
            name='tag',
            field=models.SlugField(choices=[(b'python', b'python'), (b'django', b'django'), (b'html', b'html'), (b'css', b'css'), (b'javascript', b'javascript'), (b'bootstrap', b'bootstrap')]),
        ),
    ]
