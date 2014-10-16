# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='krav',
            name='anstallda',
            field=models.CharField(default='', help_text='Ange svaret med st\xf6rre \xe4n, mindre \xe4n- och likhetstecken f\xf6ljt av siffra > x < y = 200', max_length=100, verbose_name='Anst\xe4llda'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='antal_anstallda',
            field=models.IntegerField(help_text='Ange om uppgiftskravet endast ber\xf6r f\xf6retag som har ett visst antal anst\xe4llda.', null=True, verbose_name='Antal anst\xe4llda', choices=[(1, 'Ja'), (0, 'Nej')]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='galler_from',
            field=models.DateField(help_text='Ange datom d\xe5 upppgiftskravet b\xf6rja g\xe4lla om det inte g\xe4ller nu men senare under \xe5ret.', null=True, verbose_name='G\xe4ller fr\xe5n och med', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='galler_tom',
            field=models.DateField(help_text='Ange datom d\xe5 upppgiftskravet upph\xf6r att g\xe4lla om det \xe4r k\xe4nt.', null=True, verbose_name='G\xe4lller till och med', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='lank_till_blankett',
            field=models.URLField(help_text='Ange l\xe4nk direkt till blankett', max_length=1000, null=True, verbose_name='L\xe4nk till info eller blankett', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='lank_till_etjanst',
            field=models.URLField(help_text='Ange l\xe4nk till e-tj\xe4nst', null=True, verbose_name='L\xe4nk till e-tj\xe4nst', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='lank_till_info',
            field=models.URLField(help_text='F\xf6retaget f\xe5r l\xe4sa mer om uppgiftskravet p\xe5 myndighetens webbplats', max_length=1000, null=True, verbose_name='L\xe4nk till information om uppgiftskravet', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='maskintillmaskin',
            field=models.IntegerField(help_text='Har ni ett maskin-till-maskingr\xe4nssnitt som kan anv\xe4ndas f\xf6r insamling av uppgifter i uppgiftskravet', null=True, verbose_name='Maskin-till-maskingr\xe4nssnitt', choices=[(1, 'Ja'), (0, 'Nej')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='krav',
            name='etjanst',
            field=models.IntegerField(help_text='Har ni en e-tj\xe4nst som kan anv\xe4ndas f\xf6r insamling av uppgiftskravet\n                  (dvs tj\xe4nst som m\xf6jligg\xf6r automatiserad behandling\n                  av uppgifterna)?  H\xe4r avses \xe4ven\n                  maskin-till-maskin-koppling men inte t ex\n                  pdf-blankett som m\xe5ste skrivas ut.', verbose_name='E-tj\xe4nst', choices=[(1, 'Ja'), (0, 'Nej')]),
        ),
        migrations.AlterField(
            model_name='krav',
            name='kortbeskrivning',
            field=models.TextField(help_text='Anvisning: Beskriv kortfattat vad uppgiftskravet avser s\xe5 att\n                         n\xe4ringsidkare/f\xf6retag f\xf6rst\xe5r vad som ska\n                         g\xf6ras och om det ber\xf6r dem. Max 300 tecken\n                         inkl mellanslag.', max_length=300, verbose_name='Kort beskrivning av uppgiftskravet'),
        ),
    ]
