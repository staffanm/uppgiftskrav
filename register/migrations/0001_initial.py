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
                ('kravid', models.CharField(help_text='F\xf6rklaring:ID f\xf6r uppgiftskravet.\nSka inte \xe4ndras.', unique=True, max_length=7, verbose_name='ID')),
                ('namn', models.CharField(help_text='F\xf6rklaring: Krav p\xe5 n\xe4ringsidkare/f\xf6retag till f\xf6ljd av lag,\n              f\xf6rordning eller f\xf6reskrift att l\xe4mna uppgifter till\n              myndighet.', max_length=255, verbose_name='Uppgiftskrav')),
                ('forfattning', models.CharField(help_text='Beteckning p\xe5 den lag, f\xf6rordning eller myndighetsf\xf6reskrift som\n                     uppgiftskravet finns i.\n\n                     Om f\xf6rfattningen \xe4r fel ska den inte \xe4ndras\n                     h\xe4r. Skriv ist\xe4llet korrekt f\xf6rfattning under\n                     F\xf6rfattningsst\xf6d.', verbose_name='F\xf6rfattning', max_length=50, editable=False, blank=True)),
                ('paragraf', models.CharField(help_text='F\xf6rklaring: H\xe4nvisning i aktuell f\xf6rfattning.\n\n                  Om paragrafen \xe4r fel ska den inte \xe4ndras h\xe4r. Skriv ist\xe4llet korrekt\n                  f\xf6rfattning under F\xf6rfattningsst\xf6d.', max_length=50, editable=False, blank=True)),
                ('lagrum', models.CharField(blank=True, help_text='Anvisning: Ange prim\xe4rt f\xf6rfattningsst\xf6d d\xe4r inneh\xe5llet i\n                uppgiftskravet specificeras.\n\n                F\xf6r EU-lagstiftning: Anv\xe4nd Celexnummer, artikel,\n                stycke (t ex 31993R2454 221 2).\n\n                F\xf6r nationell lagstiftning: Anv\xe4nd\n                f\xf6rfattningsf\xf6rkortning f\xf6rfattningsnummer, kapitel,\n                paragraf, stycke (t ex SJFS1995:94 15).\n\n                Om det inte g\xe5r att avg\xf6ra prim\xe4rt f\xf6rfattningsst\xf6d\n                \xe5tskilj med semikolon (;).', max_length=255, verbose_name='F\xf6rfattningsst\xf6d', validators=[register.models.not_empty])),
                ('ursprung', models.IntegerField(help_text='Vilket ursprung f\xf6rfattningen har. Antingen "EU mm" eller "Nationellt".', choices=[(1, 'Nationellt'), (2, 'EU mm')])),
                ('beskrivning', models.TextField(help_text='F\xf6rklaring: Beskrivning av uppgiftskravet.\n    \n                     Om beskrivningen \xe4r fel ska den inte \xe4ndras\n                     h\xe4r. Skriv ist\xe4llet under Kort beskrivning av\n                     uppgiftskravet.', editable=False, blank=True)),
                ('anteckning', models.TextField(help_text='Anteckning om uppgiftskravet. \n\n                    Ska inte \xe4ndras.', editable=False, blank=True)),
                ('kortbeskrivning', models.TextField(help_text='Anvisning: Beskriv kortfattat vad uppgiftskravet avser s\xe5 att\n                         n\xe4ringsidkare/f\xf6retag f\xf6rst\xe5r vad som ska\n                         g\xf6ras och om det ber\xf6r dem. Max 140 tecken\n                         inkl mellanslag.', max_length=140, verbose_name='Kort beskrivning av uppgiftskravet')),
                ('leder_till_insamling', models.IntegerField(help_text='Anvisning: Ange Ja om det \xe4r ett uppgiftskrav.\n                               Ange Nej om det inte \xe4r ett uppgiftskrav.', verbose_name='Leder till insamling fr\xe5n f\xf6retag', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('egna_noteringar', models.TextField(help_text='Anvisning: Ange egna noteringar i denna cell vid behov.\n    \n                         Noteringar fr\xe5n kartl\xe4ggningens kolumn\n                         Upph\xf6rt? ligger i denna kolumn.', blank=True)),
                ('kalenderstyrt', models.IntegerField(help_text='Ange om uppgiften l\xe4mnas in utifr\xe5n f\xf6rutbest\xe4md tidpunkt.', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('periodicitet', models.IntegerField(help_text='Ange vid vilken tidpunkt som uppgiften l\xe4mnas in om du svarat Ja\n                      under Kalenderstyrt. Om du svarat Nej under\n                      Kalenderstyrt \xe4r "Inte relevant" ifyllt.\n\n                      Ange vanligast f\xf6rekommande om det finns variationer i tidpunkter.\n\n                      V\xe4lj ett av v\xe4rdena i listan. Vid t ex \xe5rlig uppgift, ange n\xe4r p\xe5 \xe5ret.', choices=[(0, 'Inte relevant'), (1, 'Januari'), (2, 'Februari'), (3, 'Mars'), (4, 'April'), (5, 'Maj'), (6, 'Juni'), (7, 'Juli'), (8, 'Augusti'), (9, 'September'), (10, 'Oktober'), (11, 'November'), (12, 'December'), (13, 'Veckovis'), (14, 'M\xe5nadsvis'), (15, 'Kvartalsvis'), (16, '\xc5rsvis (ej s\xe4rskilt datum)')])),
                ('handelsestyrt', models.IntegerField(help_text='Ange om uppgiften l\xe4mnas in utifr\xe5n h\xe4ndelse.', verbose_name='H\xe4ndelsestyrt', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('initierande_part', models.IntegerField(help_text='Ange om myndigheten, f\xf6retaget eller b\xe5da initierar\n                          uppgiftskravet f\xf6rsta g\xe5ngen.\n\n                          Myndighetsinitierat - om myndigheten vet om\n                          att f\xf6retaget m\xe5ste g\xf6ra n\xe5got. Exempel:\n                          Skyldighet att l\xe4mna \xe5rsredovisning.\n\n                          F\xf6retagsinitierat - om myndigheten inte vet om\n                          vad f\xf6retaget ska g\xf6ra. Exempel: Anm\xe4lan till\n                            potatisregistret.', choices=[(1, 'Myndighetsinitierat'), (2, 'F\xf6retagsinitierat'), (3, 'B\xe5da')])),
                ('ovrigt_nar', models.TextField(help_text='Ange eventuella \xf6vriga upplysningar - relevanta f\xf6r kartl\xe4ggningen\n                    - som r\xf6r n\xe4r uppgiftsl\xe4mnande sker.', verbose_name='\xd6vrigt (N\xe4r)', blank=True)),
                ('arbetsgivare', models.IntegerField(help_text='Ange om uppgiftskravet endast ber\xf6r arbetsgivare.', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('storlek', models.IntegerField(help_text='Ange om uppgiftskravet endast ber\xf6r f\xf6retag eller produktion av\n                  viss storlek.', blank=True, choices=[(1, 'Ja'), (0, 'Nej')])),
                ('storlekskriterier', models.TextField(help_text='Ange storlekskriterier om du svarat Ja i kolumnen Storlek (t ex\n                           oms\xe4ttning, antal anst\xe4llda, viss\n                           lagstiftning, produktion).\n\n                           Skriv svaret som fritext i cellen.', blank=True)),
                ('ovriga_urvalskriterier', models.TextField(help_text='Beskriv \xf6vriga urvalskriterier\n                                (inte tidigare n\xe4mnda) som begr\xe4nsar\n                                vilka n\xe4ringsidkare/f\xf6retag som ska\n                                l\xe4mna uppgiftskravet.\n\n                                Skriv svaret som fritext i cellen och\n                                helst lagh\xe4nvisning t ex SFS 1995:1554\n                                9 1', blank=True)),
                ('antal_foretag', models.IntegerField(blank=True, help_text='Anvisning:\n                          \n                             Antal olika n\xe4ringsidkare/f\xf6retag som har\n                             haft \xe4renden hos myndigheten under 2012\n                             till f\xf6ljd av uppgiftskravet.\n\n                             Ombud avses inte.\n\n                             Skriv svaret med siffror i cellen.', null=True, verbose_name='Antal omfattade f\xf6retag', validators=[register.models.not_null_integer])),
                ('annan_ingivare', models.IntegerField(help_text='Ange om uppgifter som r\xf6r uppgiftskravet kan l\xe4mnas av ombud f\xf6r\n                         n\xe4ringsidkaren/f\xf6retaget (allts\xe5 n\xe5gon som\n                         har fullmakt och inte \xe4r anst\xe4lld).', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('underskrift', models.IntegerField(help_text='Kr\xe4ver uppgiftsinl\xe4mningen underskrift (p\xe5 papper eller elektroniskt)?', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('etjanst', models.IntegerField(help_text='Har ni en e-tj\xe4nst som kan anv\xe4ndas f\xf6r insamling av uppgiftskravet\n                  (dvs tj\xe4nst som m\xf6jligg\xf6r automatiserad behandling\n                  av uppgifterna)?  H\xe4r avses \xe4ven\n                  maskin-till-maskin-koppling men inte t ex\n                  pdf-blankett som m\xe5ste skrivas ut.', choices=[(1, 'Ja'), (0, 'Nej')])),
                ('svarighet_ej_etjanst', models.IntegerField(help_text='Anvisning:\n\n                             0 Uppgiftskravet kan endast fullg\xf6ras\n                             med e-tj\xe4nst.\n                                  \n                             1 Ingen information om uppgiftskravet\n                             tillg\xe4nglig p\xe5 myndighetens\n                             webbplats/er.  F\xf6retaget m\xe5ste kontakta\n                             myndigheten f\xf6r att veta vad som kr\xe4vs.\n                                  \n                             2 Information tillg\xe4nglig p\xe5\n                             myndighetens webbplats/er.  F\xf6retaget\n                             kan l\xe4sa information om tj\xe4nsten.\n                             \n                             3 Blankett tillg\xe4nglig.  F\xf6retaget kan\n                             ladda ner blankett och l\xe4mna in med brev\n                             post, fax, e-post.\n                             \n                             4 Interaktiv/smart blankett tillg\xe4nglig.\n                             F\xf6retaget kan ladda ner interaktiv\n                             (offline) blankett och l\xe4mna in med\n                             brevpost, fax, e-post.', verbose_name='Uppskattad sv\xe5righet att l\xe4mna uppgiftskravet - ej e-tj\xe4nst', choices=[(0, 'Uppgiftskravet kan endast fullg\xf6ras med e-tj\xe4nst'), (1, 'Ingen information om uppgiftskravet tillg\xe4nglig p\xe5 myndighetens webbplats/er.'), (2, 'Information om uppgiftskravet tillg\xe4nglig p\xe5 myndighetens webbplats/er.'), (3, 'Blankett tillg\xe4nglig.'), (4, 'Interaktiv/smart blankett tillg\xe4nglig.')])),
                ('svarighet_etjanst', models.IntegerField(help_text='Anvisning: \n                          5 E-tj\xe4nst\n                          F\xf6retaget kan interaktivt navigera, v\xe4gledas, ange uppgifter\n                          och l\xe4mna in online med kvittens. \n\n                          6 Maskin-till-maskin\n                          F\xf6retaget kan ansluta ett system till ett maskingr\xe4nssnitt f\xf6r att l\xe4mna in uppgifter.\n            \n                          7 Ej e-tj\xe4nst\n                          Uppgifter i uppgiftskravet kan inte samlas in via e-tj\xe4nst.\n                          \n                          V\xe4lj ett av v\xe4rdena i listan', verbose_name='Uppskattad sv\xe5righet att l\xe4mna uppgiftskravet - e-tj\xe4nst', choices=[(5, 'E-tj\xe4nst'), (6, 'Maskin-till-maskin'), (7, 'Ej e-tj\xe4nst')])),
                ('volymer_tidigare', models.IntegerField(help_text='Angiven volym i kartl\xe4ggning som genomf\xf6rdes v\xe5ren 2012.\n\n                            Ska inte \xe4ndras.', null=True, verbose_name='Volymer tidigare genomf\xf6rd kartl\xe4ggning', blank=True)),
                ('volymer_2012', models.IntegerField(blank=True, help_text='Hur m\xe5nga \xe4renden t ex anm\xe4lningar, ans\xf6kningar, unders\xf6kningar\n                        etc l\xe4mnades totalt in \xe5r 2012 f\xf6r detta uppgiftskrav?\n\n                        Skriv svaret med siffror i cellen.', null=True, verbose_name='Volymer 2012', validators=[register.models.not_null_integer])),
                ('volymer_etjanst', models.IntegerField(blank=True, help_text='Hur m\xe5nga \xe4renden t ex anm\xe4lningar, ans\xf6kningar, unders\xf6kningar etc\n                        l\xe4mnades in via e-tj\xe4nst \xe5r 2012 f\xf6r detta\n                        uppgiftskrav?', null=True, verbose_name='Varav volymer e-tj\xe4nst', validators=[register.models.not_null_integer])),
                ('ovrigt_hur', models.TextField(help_text='Finns det \xf6vrig relevant information om hur uppgiften samlas in?', verbose_name='\xd6vrigt (Hur)', blank=True)),
                ('url', models.URLField(blank=True)),
                ('ansvarig_myndighet', models.ForeignKey(related_name='ansvarig_for', verbose_name='Ansvarig myndighet', to='auth.Group', help_text='F\xf6rklaring: Myndighet som \xe4r ansvarig f\xf6r ett uppgiftskrav. Samma\n                            som kartl\xe4ggande myndighet utom i de fall\n                            insamling sker f\xf6r annan myndighets  r\xe4kning.')),
                ('bransch', models.ManyToManyField(help_text='Om uppgiftskravet endast ber\xf6r specifik bransch, ange den/dessa p\xe5\n                  den \xf6versta niv\xe5n av SNI2007.\n    \n                  Skriv en eller flera av bokst\xe4verna A-T i\n                  cellen. Bokst\xe4verna \xe5tskiljs med komma utan\n                  mellanslag.\n\n                  Om uppgiftskravet inte ber\xf6r specifik bransch, skriv\n                  bokstaven X (avser alla) i cellen.', to='register.Bransch', validators=[register.models.not_empty_list])),
                ('foretagsform', models.ManyToManyField(help_text='Om uppgiftskravet endast ber\xf6r specifika f\xf6retagsformer, ange\n                       dessa.\n    \n                       Skriv n\xe5gon eller n\xe5gra av f\xf6ljande\n                       f\xf6rkortningar E,AB,HB,KB,BRF,EK,A i cellen.\n                       Bokst\xe4verna \xe5tskiljs med komma utan mellanslag.\n                       \n                       Om uppgiftskravet inte ber\xf6r specifika\n                       f\xf6retagsformer, skriv bokstaven X (avser alla)\n                       i cellen.', to='register.Foretagsform', validators=[register.models.not_empty_list])),
                ('kartlaggande_myndighet', models.ForeignKey(related_name='kartlaggande_for', verbose_name='Kartl\xe4ggande myndighet', to='auth.Group', help_text='F\xf6rklaring:Myndighet som\n                                kartlagt uppgiftskravet.')),
            ],
            options={
                'ordering': ['id'],
                'verbose_name_plural': 'Krav',
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
            ],
            options={
                'verbose_name': 'Verksamhetsomr\xe5de',
                'verbose_name_plural': 'Verksamhetsomr\xe5den',
            },
            bases=(models.Model,),
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
            field=models.ForeignKey(blank=True, to='register.Verksamhetsomrade', help_text='F\xf6rklaring: Indelning som vissa myndigheter sj\xe4lva \xf6nskat f\xf6r att\n                           kunna dela upp arbetet.', null=True, verbose_name='Verksamhetsomr\xe5de'),
            preserve_default=True,
        ),
    ]
