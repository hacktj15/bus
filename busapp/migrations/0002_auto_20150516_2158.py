# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='slot',
            name='rotate',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='businstance',
            name='arrived',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
