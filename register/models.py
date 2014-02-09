# -*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function

from django.db import models
from django.db.models.fields import FieldDoesNotExist
from django.contrib.auth import models as authmodels
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError

class UppgiftManager(models.Manager):
    def get_by_natural_key(self, uppgiftid):
        return self.get(uppgiftid=uppgiftid)

class Uppgift(models.Model):
    objects = UppgiftManager()
    uppgiftid = models.CharField(max_length=8, unique=True)
    namn = models.CharField(max_length=100)

    def __unicode__(self):
        return "%s: %s" % (self.uppgiftid, self.namn)

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (self._meta.get_field(i), getattr(self, i))

    def natural_key(self):
        return (self.uppgiftid,)

    class Meta():
        verbose_name_plural = "Uppgifter"
        ordering = ["id"]

class VerksamhetsomradeManager(models.Manager):
    def get_by_natural_key(self, omrade):
        return self.get(omrade=omrade)

class Verksamhetsomrade(models.Model):
    objects = VerksamhetsomradeManager()
    omrade = models.CharField("Område", max_length=100, unique=True)

    def __unicode__(self):
        return self.omrade

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (self._meta.get_field(i), getattr(self, i))

    def natural_key(self):
        return (self.omrade,)

    class Meta:
        verbose_name = "Verksamhetsområde"
        verbose_name_plural = "Verksamhetsområden"

class BranschManager(models.Manager):
    def get_by_natural_key(self, snikod):
        return self.get(snikod=snikod)

class Bransch(models.Model):
    objects = BranschManager()
    snikod = models.CharField("SNI-kod", max_length=1, unique=True)
    beskrivning = models.CharField(max_length=255)

    def __unicode__(self):
        return "%s: %s" % (self.snikod, self.beskrivning)

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            try:
                yield (self._meta.get_field(i),  getattr(self, i))
            except FieldDoesNotExist: # meta.ge_all_field_names returns 'krav' for some reason...
                pass

    def natural_key(self):
        return (self.snikod,)

    class Meta:
        verbose_name_plural = "Branscher"


class ForetagsformManager(models.Manager):
    def get_by_natural_key(self, formkod):
        return self.get(formkod=formkod)

class Foretagsform(models.Model):
    objects = ForetagsformManager()
    formkod = models.CharField("Företagsformskod", max_length=3, unique=True)
    beskrivning = models.CharField(max_length=30)

    def __unicode__(self):
        return "%s: %s" % (self.formkod, self.beskrivning)

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            if hasattr(self,i):
                yield (self._meta.get_field(i), getattr(self, i))

    def natural_key(self):
        return (self.formkod,)

    class Meta:
        verbose_name = "Företagsform"
        verbose_name_plural = "Företagsformer"



class KravManager(models.Manager):
    def get_by_natural_key(self, kravid):
        return self.get(kravid=kravid)
        
# just to save some typing space...    
m2m = models.ManyToManyField
fk = models.ForeignKey
cf = models.CharField
tf = models.TextField
nbf = models.NullBooleanField
intf = models.IntegerField

class Krav(models.Model):
    
    objects = KravManager()
    OKANT = -1
    NEJ = 0
    JA = 1
    def not_empty(value):
        if not value:
            raise ValidationError("Värdet får inte vara tomt")

    def not_empty_list(value):
        if not value.all():
            raise ValidationError("Måste ange ett eller flera möjliga val")

    def not_null(value):
        if value is None:
            raise ValidationError("Antingen Ja eller Nej måste anges")

    def not_null_integer(value):
        if value is None:
            raise ValidationError("Ett tal måste anges")
    

    verksamhetsomrade = fk(Verksamhetsomrade,
                           blank=True,
                           null=True,
                           verbose_name="Verksamhetsområde",
                           help_text="""Förklaring: Indelning som vissa myndigheter själva önskat för att
                           kunna dela upp arbetet.""")

    ansvarig_myndighet = fk(authmodels.Group,
                            related_name="ansvarig_for",
                            verbose_name="Ansvarig myndighet",
                            help_text="""Förklaring: Myndighet som är ansvarig för ett uppgiftskrav. Samma
                            som kartläggande myndighet utom i de fall
                            insamling sker för annan myndighets  räkning.""")

    kartlaggande_myndighet = fk(authmodels.Group,
                                related_name="kartlaggande_for",
                                verbose_name="Kartläggande myndighet",
                                help_text="""Förklaring:Myndighet som
                                kartlagt uppgiftskravet.""")

    # actual primary key, used in Meta.unique_together    
    kravid = cf("ID",
                unique=True,
                max_length=7,
                help_text="""Förklaring:ID för uppgiftskravet.\nSka inte ändras.""") 

    # krav = cf("Krav?", blank=True, max_length=10, help_text="What?")
    
    namn = cf("Uppgiftskrav",
              max_length=255,
              help_text="""Förklaring: Krav på näringsidkare/företag till följd av lag,
              förordning eller föreskrift att lämna uppgifter till
              myndighet.""")

    forfattning = cf("Författning",
                     max_length=50,
                     editable=False,
                     blank=True,
                     help_text="""Beteckning på den lag, förordning eller myndighetsföreskrift som
                     uppgiftskravet finns i.

                     Om författningen är fel ska den inte ändras
                     här. Skriv istället korrekt författning under
                     Författningsstöd.""")

    paragraf = cf(max_length=50,
                  editable=False,
                  blank=True,
                  help_text="""Förklaring: Hänvisning i aktuell författning.

                  Om paragrafen är fel ska den inte ändras här. Skriv istället korrekt
                  författning under Författningsstöd.""")

    lagrum = cf("Författningsstöd",
                max_length=255,
                blank=True,
                help_text="""Anvisning: Ange primärt författningsstöd där innehållet i
                uppgiftskravet specificeras.

                För EU-lagstiftning: Använd Celexnummer, artikel,
                stycke (t ex 31993R2454 221 2).

                För nationell lagstiftning: Använd
                författningsförkortning författningsnummer, kapitel,
                paragraf, stycke (t ex SJFS1995:94 15).

                Om det inte går att avgöra primärt författningsstöd
                åtskilj med semikolon (;).""",
                validators=[not_empty])

    NATIONELLT=1
    EU=2
    URSPRUNG = [(NATIONELLT, "Nationellt"),
                (EU, "EU mm")]
    ursprung = intf(choices=URSPRUNG,
                  help_text="""Vilket ursprung författningen har. Antingen "EU mm" eller "Nationellt".""")

    beskrivning = tf(editable=False,
                     blank=True,
                     help_text="""Förklaring: Beskrivning av uppgiftskravet.
    
                     Om beskrivningen är fel ska den inte ändras
                     här. Skriv istället under Kort beskrivning av
                     uppgiftskravet.""")

    anteckning = tf(editable=False,
                    blank=True,
                    help_text="""Anteckning om uppgiftskravet. 

                    Ska inte ändras.""")

    kortbeskrivning = tf("Kort beskrivning av uppgiftskravet",
                         max_length=140,
                         help_text="""Anvisning: Beskriv kortfattat vad uppgiftskravet avser så att
                         näringsidkare/företag förstår vad som ska
                         göras och om det berör dem. Max 140 tecken
                         inkl mellanslag.""")

    YESNO = [(JA, 'Ja'),
             (NEJ, 'Nej')]
    leder_till_insamling = intf("Leder till insamling från företag",
                               help_text="""Anvisning: Ange Ja om det är ett uppgiftskrav.
                               Ange Nej om det inte är ett uppgiftskrav.""",
                                choices=YESNO)

    egna_noteringar = tf(blank=True,
                         help_text="""Anvisning: Ange egna noteringar i denna cell vid behov.
    
                         Noteringar från kartläggningens kolumn
                         Upphört? ligger i denna kolumn.""")

    kalenderstyrt = intf(help_text="""Ange om uppgiften lämnas in utifrån förutbestämd tidpunkt.""",
                         choices=YESNO)

    INTE_RELEVANT=0
    JANUARI=1
    FEBRUARI=2
    MARS=3
    APRIL=4
    MAJ=5
    JUNI=6
    JULI=7
    AUGUSTI=8
    SEPTEMBER=9
    OKTOBER=10
    NOVEMBER=11
    DECEMBER=12
    VECKOVIS=13
    MANADSVIS=14
    KVARTALSVIS=15
    ARSVIS=16
    periodicitet = intf(choices=[(INTE_RELEVANT, 'Inte relevant'),
                                 (JANUARI, 'Januari'),
                                 (FEBRUARI, 'Februari'),
                                 (MARS, 'Mars'),
                                 (APRIL, 'April'),
                                 (MAJ, 'Maj'),
                                 (JUNI,'Juni'),
                                 (JULI, 'Juli'),
                                 (AUGUSTI, 'Augusti'),
                                 (SEPTEMBER, 'September'),
                                 (OKTOBER, 'Oktober'),
                                 (NOVEMBER, 'November'),
                                 (DECEMBER, 'December'),
                                 (VECKOVIS, 'Veckovis'),
                                 (MANADSVIS, 'Månadsvis'),
                                 (KVARTALSVIS, 'Kvartalsvis'),
                                 (ARSVIS, 'Årsvis (ej särskilt datum)'),
                             ],
                      help_text="""Ange vid vilken tidpunkt som uppgiften lämnas in om du svarat Ja
                      under Kalenderstyrt. Om du svarat Nej under
                      Kalenderstyrt är "Inte relevant" ifyllt.

                      Ange vanligast förekommande om det finns variationer i tidpunkter.

                      Välj ett av värdena i listan. Vid t ex årlig uppgift, ange när på året.""")

    handelsestyrt = intf("Händelsestyrt",
                        help_text="""Ange om uppgiften lämnas in utifrån händelse.""",
                        choices=YESNO)


    MYNDIGHETSINITIERAT=1
    FORETAGSINITIERAT=2
    BADA=3
    initierande_part = intf(choices=((MYNDIGHETSINITIERAT, "Myndighetsinitierat"),
                                     (FORETAGSINITIERAT, "Företagsinitierat"),
                                     (BADA, "Båda")),

                            help_text="""Ange om myndigheten, företaget eller båda initierar
                          uppgiftskravet första gången.

                          Myndighetsinitierat - om myndigheten vet om
                          att företaget måste göra något. Exempel:
                          Skyldighet att lämna årsredovisning.

                          Företagsinitierat - om myndigheten inte vet om
                          vad företaget ska göra. Exempel: Anmälan till
                            potatisregistret.""")

    ovrigt_nar = tf("Övrigt (När)",
                    blank=True,
                    help_text="""Ange eventuella övriga upplysningar - relevanta för kartläggningen
                    - som rör när uppgiftslämnande sker.""")

    bransch = m2m(Bransch,
                  help_text="""Om uppgiftskravet endast berör specifik bransch, ange den/dessa på
                  den översta nivån av SNI2007.
    
                  Skriv en eller flera av bokstäverna A-T i
                  cellen. Bokstäverna åtskiljs med komma utan
                  mellanslag.

                  Om uppgiftskravet inte berör specifik bransch, skriv
                  bokstaven X (avser alla) i cellen.""",
                  validators=[not_empty_list])

    arbetsgivare = intf(help_text="""Ange om uppgiftskravet endast berör arbetsgivare.""",
                        choices=YESNO)


    foretagsform = m2m(Foretagsform,
                       help_text="""Om uppgiftskravet endast berör specifika företagsformer, ange
                       dessa.
    
                       Skriv någon eller några av följande
                       förkortningar E,AB,HB,KB,BRF,EK,A i cellen.
                       Bokstäverna åtskiljs med komma utan mellanslag.
                       
                       Om uppgiftskravet inte berör specifika
                       företagsformer, skriv bokstaven X (avser alla)
                       i cellen.""",
                       validators=[not_empty_list])

    storlek = intf(blank=True,
                  help_text="""Ange om uppgiftskravet endast berör företag eller produktion av
                  viss storlek.""",
                   choices=YESNO)


    storlekskriterier = tf(blank=True,
                           help_text="""Ange storlekskriterier om du svarat Ja i kolumnen Storlek (t ex
                           omsättning, antal anställda, viss
                           lagstiftning, produktion).

                           Skriv svaret som fritext i cellen.""")

    ovriga_urvalskriterier = tf(blank=True,
                                help_text="""Beskriv övriga urvalskriterier
                                (inte tidigare nämnda) som begränsar
                                vilka näringsidkare/företag som ska
                                lämna uppgiftskravet.

                                Skriv svaret som fritext i cellen och
                                helst laghänvisning t ex SFS 1995:1554
                                9 1""")

    antal_foretag = intf("Antal omfattade företag",
                         blank=True,
                         null=True,
                         help_text="""Anvisning:
                          
                             Antal olika näringsidkare/företag som har
                             haft ärenden hos myndigheten under 2012
                             till följd av uppgiftskravet.

                             Ombud avses inte.

                             Skriv svaret med siffror i cellen.""",
                         validators=[not_null_integer])

    annan_ingivare = intf(help_text="""Ange om uppgifter som rör uppgiftskravet kan lämnas av ombud för
                         näringsidkaren/företaget (alltså någon som
                         har fullmakt och inte är anställd).""",
                          choices=YESNO)
    

    underskrift = intf(help_text="""Kräver uppgiftsinlämningen underskrift (på papper eller elektroniskt)?""",
                       choices=YESNO)


    etjanst = intf(help_text="""Har ni en e-tjänst som kan användas för insamling av uppgiftskravet
                  (dvs tjänst som möjliggör automatiserad behandling
                  av uppgifterna)?  Här avses även
                  maskin-till-maskin-koppling men inte t ex
                  pdf-blankett som måste skrivas ut.""",
                   choices=YESNO)


    ENDAST_ETJANST=0
    INGEN_INFO_TILLGANGLIG=1
    INFO_TILLGANGLIG=2
    BLANKETT_TILLGANGLIG=3
    SMART_BLANKETT_TILLGANGLIG=4
    svarighet_ej_etjanst = intf("Uppskattad svårighet att lämna uppgiftskravet - ej e-tjänst",
                             choices=((ENDAST_ETJANST, "Uppgiftskravet kan endast fullgöras med e-tjänst"),
                                      (INGEN_INFO_TILLGANGLIG, "Ingen information om uppgiftskravet tillgänglig på myndighetens webbplats/er."),
                                      (INFO_TILLGANGLIG, "Information om uppgiftskravet tillgänglig på myndighetens webbplats/er."),
                                      (BLANKETT_TILLGANGLIG, "Blankett tillgänglig."),
                                      (SMART_BLANKETT_TILLGANGLIG, "Interaktiv/smart blankett tillgänglig.")),
                             help_text="""Anvisning:

                             0 Uppgiftskravet kan endast fullgöras
                             med e-tjänst.
                                  
                             1 Ingen information om uppgiftskravet
                             tillgänglig på myndighetens
                             webbplats/er.  Företaget måste kontakta
                             myndigheten för att veta vad som krävs.
                                  
                             2 Information tillgänglig på
                             myndighetens webbplats/er.  Företaget
                             kan läsa information om tjänsten.
                             
                             3 Blankett tillgänglig.  Företaget kan
                             ladda ner blankett och lämna in med brev
                             post, fax, e-post.
                             
                             4 Interaktiv/smart blankett tillgänglig.
                             Företaget kan ladda ner interaktiv
                             (offline) blankett och lämna in med
                             brevpost, fax, e-post.""")

    ETJANST=5
    MASKIN_TILL_MASKIN=6
    EJ_ETJANST=7
    svarighet_etjanst = intf("Uppskattad svårighet att lämna uppgiftskravet - e-tjänst",
                          choices=((ETJANST,"E-tjänst"),
                                   (MASKIN_TILL_MASKIN, "Maskin-till-maskin"),
                                   (EJ_ETJANST, "Ej e-tjänst")),
                          help_text="""Anvisning: 
                          5 E-tjänst
                          Företaget kan interaktivt navigera, vägledas, ange uppgifter
                          och lämna in online med kvittens. 

                          6 Maskin-till-maskin
                          Företaget kan ansluta ett system till ett maskingränssnitt för att lämna in uppgifter.
            
                          7 Ej e-tjänst
                          Uppgifter i uppgiftskravet kan inte samlas in via e-tjänst.
                          
                          Välj ett av värdena i listan""")

    volymer_tidigare = intf("Volymer tidigare genomförd kartläggning",
                            blank=True,
                            null=True,
                            help_text="""Angiven volym i kartläggning som genomfördes våren 2012.

                            Ska inte ändras.""")

    volymer_2012 = intf("Volymer 2012",
                        blank=True,
                        null=True,
                        help_text="""Hur många ärenden t ex anmälningar, ansökningar, undersökningar
                        etc lämnades totalt in år 2012 för detta uppgiftskrav?

                        Skriv svaret med siffror i cellen.""",
                        validators=[not_null_integer])

    volymer_etjanst = intf("Varav volymer e-tjänst",
                           blank=True,
                           null=True,
                        help_text="""Hur många ärenden t ex anmälningar, ansökningar, undersökningar etc
                        lämnades in via e-tjänst år 2012 för detta
                        uppgiftskrav?""",
                           validators=[not_null_integer])

    ovrigt_hur = tf("Övrigt (Hur)",
                    blank=True,
                    help_text="""Finns det övrig relevant information om hur uppgiften samlas in?""")

    url = models.URLField(blank=True) # link to etjänst
    uppgifter = models.ManyToManyField(Uppgift, blank=True, validators=[not_empty_list])

    def __unicode__(self):
        return "%s: %s" % (self.kravid, self.namn)

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            #if i == "initierande_part":
            #    from pudb import set_trace; set_trace()
            yield (self._meta.get_field(i), getattr(self, i))

    def natural_key(self):
        return (self.kravid,)

    def get_absolute_url(self):
        return reverse('register:krav-detail', args=[self.kravid])

    def valid(self):
        try:
            self.full_clean()
            return True
        except ValidationError:
            return False
    valid.boolean = True
    valid.short_description = "Fullständigt"

    class Meta():
        verbose_name_plural = "Krav"
        ordering = ["id"]
    
