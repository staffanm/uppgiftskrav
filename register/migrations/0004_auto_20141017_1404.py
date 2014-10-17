# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20141017_1203'),
    ]

    operations = [
        migrations.AddField(
            model_name='krav',
            name='blankett',
            field=models.IntegerField(help_text='Har ni en elektronisk blankett (t ex PDF-blankett) som kan fyllas i och l\xe4mnas in med brev, fax, e-post', null=True, verbose_name='Elektronisk blankett', choices=[(1, 'Ja'), (0, 'Nej')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='krav',
            name='aktivt',
            field=models.IntegerField(default=0, help_text='\xc4r uppgiftskravet aktuellt, g\xe4llande och fullst\xe4ndigt (inte under redigering)?', verbose_name='Publicerat', choices=[(1, 'Ja'), (0, 'Nej')]),
        ),
        migrations.AlterField(
            model_name='krav',
            name='bransch',
            field=models.ManyToManyField(help_text='Om uppgiftskravet endast ber\xf6r specifik bransch, ange den/dessa p\xe5\n                  den \xf6versta niv\xe5n av SNI2007.\n\n                  Om uppgiftskravet inte ber\xf6r specifik bransch, ange X (avser alla).', to=b'register.Bransch', validators=[register.models.not_empty_list]),
        ),
        migrations.AlterField(
            model_name='krav',
            name='etjanst',
            field=models.IntegerField(help_text='Har ni en e-tj\xe4nst som kan anv\xe4ndas f\xf6r insamling av uppgiftskravet\n                  (dvs tj\xe4nst som m\xf6jligg\xf6r automatiserad behandling\n                  av uppgifterna)?  H\xe4r inte t ex\n                  pdf-blankett som m\xe5ste skrivas ut.', verbose_name='E-tj\xe4nst', choices=[(1, 'Ja'), (0, 'Nej')]),
        ),
        migrations.AlterField(
            model_name='krav',
            name='foretagsform',
            field=models.ManyToManyField(help_text='Om uppgiftskravet endast ber\xf6r specifika f\xf6retagsformer, ange\n                       dessa.\n\n                       Om uppgiftskravet inte ber\xf6r specifika\n                       f\xf6retagsformer, ange X (avser alla).', to=b'register.Foretagsform', validators=[register.models.not_empty_list]),
        ),
        migrations.AlterField(
            model_name='krav',
            name='lank_till_blankett',
            field=models.URLField(help_text='Ange l\xe4nk direkt till blankett i det fall det finns, annars l\xe4mna tomt.', max_length=1000, null=True, verbose_name='L\xe4nk till blankett', blank=True),
        ),
        migrations.AlterField(
            model_name='krav',
            name='lank_till_etjanst',
            field=models.URLField(help_text='Ange l\xe4nk till e-tj\xe4nsti det fall det finns, annars l\xe4mna tomt.', null=True, verbose_name='L\xe4nk till e-tj\xe4nst', blank=True),
        ),
    ]
