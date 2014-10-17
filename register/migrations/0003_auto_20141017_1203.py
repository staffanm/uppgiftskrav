# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20141016_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='krav',
            name='url',
        ),
        migrations.AddField(
            model_name='krav',
            name='aktivt',
            field=models.IntegerField(default=0, help_text='\xc4r uppgiftskravet aktuellt, g\xe4llande och fullst\xe4ndigt (inte under redigering)?', verbose_name='Aktivt', choices=[(1, 'Ja'), (0, 'Nej')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='krav',
            name='namn',
            field=models.CharField(help_text='Ben\xe4mning p\xe5 uppgiftskravet gentemot f\xf6retaget', max_length=255, verbose_name='Uppgiftskravsnamn'),
        ),
    ]
