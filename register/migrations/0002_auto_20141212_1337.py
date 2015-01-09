# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='krav',
            name='periodicitet',
            field=models.ManyToManyField(help_text='Ange vid vilken tidpunkt som uppgiften l\xe4mnas in.\n\n                       Ange vanligast f\xf6rekommande om det finns variationer i tidpunkter.\n\n                       V\xe4lj ett av v\xe4rdena i listan. Vid t ex \xe5rlig uppgift, ange n\xe4r p\xe5 \xe5ret.', to=b'register.Periodicitet', null=True, blank=True),
        ),
    ]
