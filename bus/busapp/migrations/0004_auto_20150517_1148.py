# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('busapp', '0003_bususer'),
    ]

    operations = [
        migrations.AddField(
            model_name='bususer',
            name='bus_name',
            field=models.CharField(max_length=64, default=False),
        ),
        migrations.AddField(
            model_name='bususer',
            name='tjusername',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
