# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0002_auto_20141212_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='krav',
            name='kortbeskrivning',
            field=models.TextField(help_text='Beskriv kortfattat vad uppgiftskravet\n                         avser s\xe5 att f\xf6retag f\xf6rst\xe5r vad som ska\n                         g\xf6ras och om det ber\xf6r dem. Max 600 tecken\n                         inkl mellanslag.', max_length=600, verbose_name='Kort beskrivning av uppgiftskravet', blank=True),
        ),
    ]
