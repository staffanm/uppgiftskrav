# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import register.models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlankettURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Blankettl\xe4nk',
                'verbose_name_plural': 'Blankettl\xe4nkar',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Bransch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('snikod', models.CharField(unique=True, max_length=1, verbose_name='SNI-kod')),
                ('beskrivning', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name_plural': 'Branscher',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EtjanstURL',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
            ],
            options={
                'verbose_name': 'Etj\xe4nstl\xe4nk',
                'verbose_name_plural': 'Etj\xe4nstl\xe4nkar',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Foretagsform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('formkod', models.CharField(unique=True, max_length=3, verbose_name='F\xf6retagsformskod')),
                ('beskrivning', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'F\xf6retagsform',
                'verbose_name_plural': 'F\xf6retagsformer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Krav',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('kravid', models.CharField(help_text='ID f\xf6r uppgiftskravet.\nSka inte \xe4ndras.', unique=True, max_length=7, verbose_name='ID')),
                ('namn', models.CharField(help_text='Tydlig och enkel ben\xe4mning p\xe5 uppgiftskravet s\xe5 att f\xf6retaget f\xf6rst\xe5r vad det inneb\xe4r.', max_length=255, verbose_name='Uppgiftskrav')),
                ('forfattning', models.CharField(help_text='Beteckning p\xe5 den lag, f\xf6rordning eller myndighetsf\xf6reskrift som\n                     uppgiftskravet finns i.\n\n                     Om f\xf6rfattningen \xe4r fel ska den inte \xe4ndras\n                     h\xe4r. Skriv ist\xe4llet korrekt f\xf6rfattning under\n                     F\xf6rfattningsst\xf6d.', verbose_name='F\xf6rfattning', max_length=50, editable=False, blank=True)),
                ('paragraf', models.CharField(help_text='H\xe4nvisning i aktuell f\xf6rfattning.\n\n                  Om paragrafen \xe4r fel ska den inte \xe4ndras h\xe4r. Skriv ist\xe4llet korrekt\n                  f\xf6rfattning under F\xf6rfattningsst\xf6d.', max_length=50, editable=False, blank=True)),
                ('lagrum', models.CharField(blank=True, help_text='Ange prim\xe4rt f\xf6rfattningsst\xf6d d\xe4r inneh\xe5llet i\n                uppgiftskravet specificeras.\n\n                F\xf6r EU-lagstiftning: Anv\xe4nd Celexnummer, artikel,\n                stycke d\xe4refter ev bilaga (t ex 31993R2454 221 2).\n\n                F\xf6r nationell lagstiftning: Anv\xe4nd\n                f\xf6rfattningssamlingsf\xf6rkortning f\xf6rfattningsnummer, kapitel,\n                paragraf, stycke d\xe4refter ev. bilaga (t ex SJFS1995:94 15).\n\n                Om det inte g\xe5r att avg\xf6ra prim\xe4rt f\xf6rfattningsst\xf6d\n                \xe5tskilj med semikolon (;).', max_length=1000, verbose_name='F\xf6rfattningsst\xf6d', validators=[register.models.not_empty])),
                ('ursprung', models.IntegerField(blank=True, help_text='Vilket ursprung f\xf6rfattningen har. Antingen "EU mm" eller "Nationellt"', null=True, choices=[(1, 'Nationellt'), (2, 'EU mm')])),
                ('omfattas_av_tjdir', models.BooleanField(default=False, help_text='Detta uppgiftskrav omfattas av EU:s tj\xe4nstedirektiv (2006/123/EG)', verbose_name='Omfattas av tj\xe4nstedirektivet')),
                ('beskrivning', models.TextField(help_text='Beskrivning av uppgiftskravet.\n    \n                     Om beskrivningen \xe4r fel ska den inte \xe4ndras\n                     h\xe4r. Skriv ist\xe4llet under Kort beskrivning av\n                     uppgiftskravet.', editable=False, blank=True)),
                ('anteckning', models.TextField(help_text='Anteckning om uppgiftskravet.\n\n                    Ska inte \xe4ndras.', editable=False, blank=True)),
                ('kortbeskrivning', models.TextField(help_text='Beskriv kortfattat vad uppgiftskravet\n                         avser s\xe5 att f\xf6retag f\xf6rst\xe5r vad som ska\n                         g\xf6ras och om det ber\xf6r dem. Max 300 tecken\n                         inkl mellanslag.', max_length=300, verbose_name='Kort beskrivning av uppgiftskravet')),
                ('lank_till_info', models.URLField(help_text='Ange l\xe4nk till st\xe4lle p\xe5 myndighetens webbplats d\xe4r information om uppgiftskravet framg\xe5r och d\xe4r f\xf6retaget kan l\xe4sa mer om uppgiftskravet.', max_length=1000, null=True, verbose_name='L\xe4nk till information om uppgiftskravet', blank=True)),
                ('leder_till_insamling', models.IntegerField(help_text='Ange Ja om det \xe4r ett uppgiftskrav.\n                               Ange Nej om det inte \xe4r ett uppgiftskrav.', verbose_name='Leder till insamling fr\xe5n f\xf6retag', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('galler_from', models.DateField(help_text='Ange datum d\xe5 upppgiftskravet b\xf6rja g\xe4lla om det inte g\xe4ller nu men senare.', null=True, verbose_name='G\xe4ller fr\xe5n och med', blank=True)),
                ('galler_tom', models.DateField(help_text='Ange datum d\xe5 upppgiftskravet upph\xf6r att g\xe4lla om det \xe4r k\xe4nt.', null=True, verbose_name='G\xe4ller till och med', blank=True)),
                ('egna_noteringar', models.TextField(help_text='Ange egna noteringar i denna cell vid behov.', blank=True)),
                ('kalenderstyrt', models.IntegerField(help_text='Ange om uppgiften l\xe4mnas in utifr\xe5n f\xf6rutbest\xe4md tidpunkt.', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('handelsestyrt', models.IntegerField(blank=True, help_text='Ange om uppgiften l\xe4mnas in utifr\xe5n h\xe4ndelse.', null=True, verbose_name='H\xe4ndelsestyrt', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('initierande_part', models.IntegerField(help_text='Ange om myndigheten eller f\xf6retaget \n                          initierar uppgiftskravet f\xf6rsta g\xe5ngen.', choices=[(1, 'Myndighetsinitierat'), (2, 'F\xf6retagsinitierat')])),
                ('ovrigt_nar', models.TextField(help_text='Ange eventuella \xf6vriga upplysningar - relevanta f\xf6r kartl\xe4ggningen\n                    - som r\xf6r n\xe4r uppgiftsl\xe4mnande sker.', verbose_name='\xd6vrigt (N\xe4r)', blank=True)),
                ('beror_bransch', models.IntegerField(verbose_name='Ber\xf6r specifik bransch', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('arbetsgivare', models.IntegerField(help_text='Ange om uppgiftskravet endast ber\xf6r arbetsgivare.', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('antal_anstallda', models.IntegerField(help_text='Ange om uppgiftskravet endast ber\xf6r f\xf6retag som har ett visst antal anst\xe4llda.', null=True, verbose_name='Antal anst\xe4llda', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('anstallda', models.CharField(default='', help_text='Ange svaret med st\xf6rre \xe4n, mindre \xe4n- och likhetstecken f\xf6ljt av siffra > x < y = 200', max_length=100, verbose_name='Anst\xe4llda')),
                ('beror_foretagsform', models.IntegerField(verbose_name='Ber\xf6r specifika f\xf6retagsformer', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('storlek', models.IntegerField(blank=True, help_text='Ange om uppgiftskravet endast ber\xf6r f\xf6retag eller produktion av viss storlek.', null=True, choices=[(1, 'Ja'), (0, 'Nej')])),
                ('storlekskriterier', models.TextField(help_text='Ange storlekskriterier om du svarat Ja i kolumnen Storlek (t ex\n                           oms\xe4ttning, antal anst\xe4llda, viss\n                           lagstiftning, produktion).\n\n                           Skriv svaret som fritext i cellen.', blank=True)),
                ('ovriga_urvalskriterier', models.TextField(help_text='Beskriv \xf6vriga urvalskriterier\n                                (inte tidigare n\xe4mnda) som begr\xe4nsar\n                                vilka n\xe4ringsidkare/f\xf6retag som ska\n                                l\xe4mna uppgiftskravet.\n\n                                Skriv svaret som fritext i cellen och\n                                helst lagh\xe4nvisning t ex SFS 1995:1554\n                                9 1', blank=True)),
                ('antal_foretag', models.IntegerField(blank=True, help_text='Antal olika n\xe4ringsidkare/f\xf6retag som har\n                             haft \xe4renden hos myndigheten under 2012\n                             till f\xf6ljd av uppgiftskravet.\n\n                             Ombud avses inte.\n\n                             Skriv svaret med siffror i cellen.', null=True, verbose_name='Antal omfattade f\xf6retag', validators=[register.models.not_null_integer])),
                ('annan_ingivare', models.IntegerField(help_text='Ange om uppgifter som r\xf6r uppgiftskravet kan l\xe4mnas av ombud f\xf6r\n                         f\xf6retaget (allts\xe5 n\xe5gon som\n                         har fullmakt och inte \xe4r anst\xe4lld).', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('underskrift', models.IntegerField(blank=True, help_text='Kr\xe4ver uppgiftsinl\xe4mningen underskrift (p\xe5 papper eller elektroniskt)?', null=True, choices=[(1, 'Ja'), (0, 'Nej')])),
                ('etjanst', models.IntegerField(help_text='Har ni en e-tj\xe4nst som kan anv\xe4ndas f\xf6r insamling av uppgiftskravet\n                  (dvs tj\xe4nst som m\xf6jligg\xf6r automatiserad behandling\n                  av uppgifterna)?  H\xe4r avses inte t ex\n                  pdf-blankett som m\xe5ste skrivas ut.', verbose_name='E-tj\xe4nst', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('blankett', models.IntegerField(help_text='Har ni en elektronisk blankett (t ex PDF-blankett) som kan fyllas i och l\xe4mnas in med brev, fax, e-post?', null=True, verbose_name='Elektronisk blankett', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('maskintillmaskin', models.IntegerField(help_text='Har ni ett maskin-till-maskingr\xe4nssnitt som kan anv\xe4ndas f\xf6r insamling av uppgifter i uppgiftskravet?', null=True, verbose_name='Maskin-till-maskingr\xe4nssnitt', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('svarighet_ej_etjanst', models.IntegerField(blank=True, help_text='0 Uppgiftskravet kan endast fullg\xf6ras\n                             med e-tj\xe4nst.\n                                  \n                             1 Ingen information om uppgiftskravet\n                             tillg\xe4nglig p\xe5 myndighetens\n                             webbplats/er.  F\xf6retaget m\xe5ste kontakta\n                             myndigheten f\xf6r att veta vad som kr\xe4vs.\n                                  \n                             2 Information tillg\xe4nglig p\xe5\n                             myndighetens webbplats/er.  F\xf6retaget\n                             kan l\xe4sa information om tj\xe4nsten.\n                             \n                             3 Blankett tillg\xe4nglig.  F\xf6retaget kan\n                             ladda ner blankett och l\xe4mna in med brev\n                             post, fax, e-post.\n                             \n                             4 Interaktiv/smart blankett tillg\xe4nglig.\n                             F\xf6retaget kan ladda ner interaktiv\n                             (offline) blankett och l\xe4mna in med\n                             brevpost, fax, e-post.', null=True, verbose_name='Uppskattad sv\xe5righet att l\xe4mna uppgiftskravet - ej e-tj\xe4nst', choices=[(0, 'Uppgiftskravet kan endast fullg\xf6ras med e-tj\xe4nst'), (1, 'Ingen information om uppgiftskravet tillg\xe4nglig p\xe5 myndighetens webbplats/er.'), (2, 'Information om uppgiftskravet tillg\xe4nglig p\xe5 myndighetens webbplats/er.'), (3, 'Blankett tillg\xe4nglig.'), (4, 'Interaktiv/smart blankett tillg\xe4nglig.')])),
                ('svarighet_etjanst', models.IntegerField(blank=True, help_text='5 E-tj\xe4nst\n                          F\xf6retaget kan interaktivt navigera, v\xe4gledas, ange uppgifter\n                          och l\xe4mna in online med kvittens. \n\n                          6 Maskin-till-maskin\n                          F\xf6retaget kan ansluta ett system till ett maskingr\xe4nssnitt f\xf6r att l\xe4mna in uppgifter.\n            \n                          7 Ej e-tj\xe4nst\n                          Uppgifter i uppgiftskravet kan inte samlas in via e-tj\xe4nst.\n                          \n                          V\xe4lj ett av v\xe4rdena i listan', null=True, verbose_name='Uppskattad sv\xe5righet att l\xe4mna uppgiftskravet - e-tj\xe4nst', choices=[(5, 'E-tj\xe4nst'), (6, 'Maskin-till-maskin'), (7, 'Ej e-tj\xe4nst')])),
                ('volymer_tidigare', models.IntegerField(help_text='Angiven volym i kartl\xe4ggning som genomf\xf6rdes v\xe5ren 2012.\n\n                            Ska inte \xe4ndras.', null=True, verbose_name='Volymer tidigare genomf\xf6rd kartl\xe4ggning', blank=True)),
                ('volymer_2012', models.IntegerField(blank=True, help_text='Hur m\xe5nga \xe4renden t ex anm\xe4lningar, ans\xf6kningar, unders\xf6kningar\n                        etc l\xe4mnades totalt in \xe5r 2012 f\xf6r detta uppgiftskrav?\n\n                        Skriv svaret med siffror i cellen.', null=True, verbose_name='Volymer 2012', validators=[register.models.not_null_integer])),
                ('volymer_etjanst', models.IntegerField(blank=True, help_text='Hur m\xe5nga \xe4renden t ex anm\xe4lningar, ans\xf6kningar, unders\xf6kningar etc\n                        l\xe4mnades in via e-tj\xe4nst \xe5r 2012 f\xf6r detta\n                        uppgiftskrav?', null=True, verbose_name='Varav volymer e-tj\xe4nst', validators=[register.models.not_null_integer])),
                ('ovrigt_hur', models.TextField(help_text='Finns det \xf6vrig relevant information om hur uppgiften samlas in?', verbose_name='\xd6vrigt (Hur)', blank=True)),
                ('aktivt', models.IntegerField(default=0, help_text='\xc4r uppgiftskravet aktuellt, g\xe4llande och fullst\xe4ndigt (inte under redigering)?', verbose_name='Publicerat', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('avgransad', models.BooleanField(default=False, help_text='Avgr\xe4nsat enligt villkor i anvisningarnas stycke om avgr\xe4nsning.', verbose_name='Avgr\xe4nsat')),
                ('ansvarig_myndighet', models.ForeignKey(related_name='ansvarig_for', verbose_name='Ansvarig myndighet', to='auth.Group', help_text='Myndighet som \xe4r ansvarig f\xf6r ett uppgiftskrav. Samma\n                            som kartl\xe4ggande myndighet utom i de fall\n                            insamling sker f\xf6r annan myndighets  r\xe4kning.')),
                ('bransch', models.ManyToManyField(blank=True, help_text='Om uppgiftskravet endast ber\xf6r specifik bransch, ange den/dessa p\xe5\n                  den \xf6versta niv\xe5n av SNI2007.', null=True, to='register.Bransch', validators=[register.models.not_empty_list])),
                ('foretagsform', models.ManyToManyField(blank=True, help_text='Om uppgiftskravet endast ber\xf6r specifika f\xf6retagsformer, ange\n                       dessa.', null=True, to='register.Foretagsform', validators=[register.models.not_empty_list])),
                ('kartlaggande_myndighet', models.ForeignKey(related_name='kartlaggande_for', verbose_name='Kartl\xe4ggande myndighet', to='auth.Group', help_text='Myndighet som\n                                kartlagt uppgiftskravet.')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'Krav',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Kravomrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('omrade', models.CharField(unique=True, max_length=100, verbose_name='Kravomr\xe5de')),
                ('beskrivning', models.TextField(verbose_name='Beskrivning')),
                ('myndighet', models.ForeignKey(related_name='kravomrade_for', to='auth.Group', help_text='Myndighet som har definierat kravomr\xe5det')),
            ],
            options={
                'verbose_name': 'Kravomr\xe5de',
                'verbose_name_plural': 'Kravomr\xe5den',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Periodicitet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beskrivning', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Periodiciteter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Uppgift',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uppgiftid', models.CharField(unique=True, max_length=8)),
                ('namn', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'Uppgifter',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Verksamhetsomrade',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('omrade', models.CharField(unique=True, max_length=100, verbose_name='Omr\xe5de')),
                ('myndighet', models.ForeignKey(related_name='verksamhetsomrade_for', to='auth.Group', help_text='Myndighet som har verksamhetsomr\xe5det')),
            ],
            options={
                'verbose_name': 'Verksamhetsomr\xe5de',
                'verbose_name_plural': 'Verksamhetsomr\xe5den',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='krav',
            name='kravomrade',
            field=models.ForeignKey(blank=True, to='register.Kravomrade', help_text='Om uppgiftskravet h\xf6r till ett redan befintligt och av myndigheten definierat kravomr\xe5de eller liknande, ange det om det g\xe5r att \xe5teranv\xe4nda och visa mot kund.', null=True, verbose_name='Kravomr\xe5de'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='periodicitet',
            field=models.ManyToManyField(help_text='Ange vid vilken tidpunkt som uppgiften l\xe4mnas in om du svarat Ja\n                       under Kalenderstyrt. Om du svarat Nej under\n                       Kalenderstyrt \xe4r "Inte relevant" ifyllt.\n\n                       Ange vanligast f\xf6rekommande om det finns variationer i tidpunkter.\n\n                       V\xe4lj ett av v\xe4rdena i listan. Vid t ex \xe5rlig uppgift, ange n\xe4r p\xe5 \xe5ret.', to='register.Periodicitet', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='uppgifter',
            field=models.ManyToManyField(to='register.Uppgift', blank=True, validators=[register.models.not_empty_list]),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='krav',
            name='verksamhetsomrade',
            field=models.ForeignKey(blank=True, to='register.Verksamhetsomrade', help_text='Indelning som vissa myndigheter sj\xe4lva \xf6nskat f\xf6r att kunna dela upp arbetet.', null=True, verbose_name='Verksamhetsomr\xe5de'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='etjansturl',
            name='krav',
            field=models.ForeignKey(to='register.Krav'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='blanketturl',
            name='krav',
            field=models.ForeignKey(to='register.Krav'),
            preserve_default=True,
        ),
    ]
