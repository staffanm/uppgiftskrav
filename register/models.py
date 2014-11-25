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
    myndighet = models.ForeignKey(authmodels.Group,
                                  related_name="verksamhetsomrade_for",
                                  help_text="Myndighet som har verksamhetsområdet")

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


class KravomradeManager(models.Manager):
    def get_by_natural_key(self, omrade):
        return self.get(omrade=omrade)

class Kravomrade(models.Model):
    objects = KravomradeManager()
    omrade = models.CharField("Kravområde", max_length=100, unique=True)
    beskrivning = models.TextField("Beskrivning")
    myndighet = models.ForeignKey(authmodels.Group,
                                  related_name="kravomrade_for",
                                  help_text="Myndighet som har definierat kravområdet")

    def __unicode__(self):
        return self.omrade

    def __iter__(self):
        for i in self._meta.get_all_field_names():
            yield (self._meta.get_field(i), getattr(self, i))

    def natural_key(self):
        return (self.omrade,)

    class Meta:
        verbose_name = "Kravområde"
        verbose_name_plural = "Kravområden"

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
            if hasattr(self, i):
                yield (self._meta.get_field(i), getattr(self, i))

    def natural_key(self):
        return (self.formkod,)

    class Meta:
        verbose_name = "Företagsform"
        verbose_name_plural = "Företagsformer"


class Periodicitet(models.Model):
    beskrivning = models.CharField(max_length=50)

    def __unicode__(self):
        return "%s" % self.beskrivning

    class Meta:
        verbose_name_plural = "Periodiciteter"


class KravManager(models.Manager):
    def get_by_natural_key(self, kravid):
        return self.get(kravid=kravid)
        
# just to save some typing space...    
m2m = models.ManyToManyField
fk = models.ForeignKey
cf = models.CharField
tf = models.TextField
nbf = models.NullBooleanField
bf = models.BooleanField
intf = models.IntegerField
url = models.URLField
datef = models.DateField


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



class Krav(models.Model):
    
    objects = KravManager()
    OKANT = -1
    NEJ = 0
    JA = 1

    verksamhetsomrade = fk(Verksamhetsomrade,
                           blank=True,
                           null=True,
                           verbose_name="Verksamhetsområde",
                           help_text="Indelning som vissa myndigheter själva "
                                     "önskat för att kunna dela upp arbetet.")

    kravomrade = fk(Kravomrade,
                    blank=True,
                    null=True,
                    verbose_name="Kravområde",
                    help_text="Om uppgiftskravet hör till ett redan befintligt och av myndigheten definierat kravområde eller liknande, ange det om det går att återanvända och visa mot kund.")

    ansvarig_myndighet = fk(authmodels.Group,
                            blank=True,
                            null=True,
                            related_name="ansvarig_for",
                            verbose_name="Ansvarig myndighet",
                            help_text="""Myndighet som är ansvarig för ett uppgiftskrav. Samma
                            som kartläggande myndighet utom i de fall
                            insamling sker för annan myndighets  räkning.""")

    kartlaggande_myndighet = fk(authmodels.Group,
                                blank=True,
                                null=True,
                                related_name="kartlaggande_for",
                                verbose_name="Kartläggande myndighet",
                                help_text="""Myndighet som
                                kartlagt uppgiftskravet.""")

    # actual primary key, used in Meta.unique_together    
    kravid = cf("ID",
                unique=True,
                max_length=7,
                help_text="""ID för uppgiftskravet.\nSka inte ändras.""") 

    namn = cf("Uppgiftskrav",
              max_length=255,
              blank=True,
              help_text="""Tydlig och enkel benämning på uppgiftskravet så att företaget förstår vad det innebär.""")

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
                  help_text="""Hänvisning i aktuell författning.

                  Om paragrafen är fel ska den inte ändras här. Skriv istället korrekt
                  författning under Författningsstöd.""")

    lagrum = cf("Författningsstöd",
                max_length=1000,
                blank=True,
                help_text="""Ange primärt författningsstöd där innehållet i
                uppgiftskravet specificeras.

                För EU-lagstiftning: Använd Celexnummer, artikel,
                stycke därefter ev bilaga (t ex 31993R2454 221 2).

                För nationell lagstiftning: Använd
                författningssamlingsförkortning författningsnummer, kapitel,
                paragraf, stycke därefter ev. bilaga (t ex SJFS1995:94 15).

                Om det inte går att avgöra primärt författningsstöd
                åtskilj med semikolon (;).""",
                validators=[not_empty])

    NATIONELLT=1
    EU=2
    URSPRUNG = [(NATIONELLT, "Nationellt"),
                (EU, "EU mm")]
    ursprung = intf(choices=URSPRUNG,
                    blank=True,
                    null=True,
                    help_text='Vilket ursprung författningen har. '
                              'Antingen "EU mm" eller "Nationellt"')

    omfattas_av_tjdir = bf("Omfattas av tjänstedirektivet",
                           default=False,
                           help_text="Detta uppgiftskrav omfattas av EU:s tjänstedirektiv (2006/123/EG)")


    beskrivning = tf(editable=False,
                     blank=True,
                     help_text="""Beskrivning av uppgiftskravet.
    
                     Om beskrivningen är fel ska den inte ändras
                     här. Skriv istället under Kort beskrivning av
                     uppgiftskravet.""")

    anteckning = tf(editable=False,
                    blank=True,
                    help_text="""Anteckning om uppgiftskravet.

                    Ska inte ändras.""")

    kortbeskrivning = tf("Kort beskrivning av uppgiftskravet",
                         blank=True,
                         max_length=300,
                         help_text="""Beskriv kortfattat vad uppgiftskravet
                         avser så att företag förstår vad som ska
                         göras och om det berör dem. Max 300 tecken
                         inkl mellanslag.""")
    lank_till_info = url("Länk till information om uppgiftskravet",
                         max_length=1000,  # myndigheters URL:ar...
                         blank=True,
                         null=True,
                         help_text="Ange länk till ställe på myndighetens "
                                   "webbplats där information om "
                                   "uppgiftskravet framgår och där företaget "
                                   "kan läsa mer om uppgiftskravet.")
    JANEJ = [
             (JA, 'Ja'),
             (NEJ, 'Nej')]
    leder_till_insamling = intf("Leder till insamling från företag",
                                help_text="""Ange Ja om det är ett uppgiftskrav. Ange Nej om det inte är ett uppgiftskrav.""",
                                blank=True,
                                null=True,
                                choices=JANEJ)
    
    galler_from = datef("Gäller från och med",
                        null=True,
                        blank=True,
                        help_text="Ange datum då upppgiftskravet börja gälla "
                                  "om det inte gäller nu men senare.")
    galler_tom = datef("Gäller till och med",
                       null=True,
                       blank=True,
                       help_text="""Ange datum då upppgiftskravet upphör att gälla om det är känt.""")

    egna_noteringar = tf(blank=True,
                         help_text="""Ange egna noteringar i denna cell vid behov.""")

    kalenderstyrt = intf(help_text="""Ange om uppgiften lämnas in utifrån förutbestämd tidpunkt.""",
                         blank=True,
                         null=True,
                         choices=JANEJ)

#    INTE_RELEVANT=0
#    JANUARI=1
#    FEBRUARI=2
#    MARS=3
#    APRIL=4
#    MAJ=5
#    JUNI=6
#    JULI=7
#    AUGUSTI=8
#    SEPTEMBER=9
#    OKTOBER=10
#    NOVEMBER=11
#    DECEMBER=12
#    VECKOVIS=13
#    MANADSVIS=14
#    KVARTALSVIS=15
#    ARSVIS=16
#    # FIXME: ska vara möjligt att ange flera av dessa? m2m?
#    periodicitet = intf(choices=[(INTE_RELEVANT, 'Inte relevant'),
#                                 (JANUARI, 'Januari'),
#                                 (FEBRUARI, 'Februari'),
#                                 (MARS, 'Mars'),
#                                 (APRIL, 'April'),
#                                 (MAJ, 'Maj'),
#                                 (JUNI, 'Juni'),
#                                 (JULI, 'Juli'),
#                                 (AUGUSTI, 'Augusti'),
#                                 (SEPTEMBER, 'September'),
#                                 (OKTOBER, 'Oktober'),
#                                 (NOVEMBER, 'November'),
#                                 (DECEMBER, 'December'),
#                                 (VECKOVIS, 'Veckovis'),
#                                 (MANADSVIS, 'Månadsvis'),
#                                 (KVARTALSVIS, 'Kvartalsvis'),
#                                 (ARSVIS, 'Årsvis (ej särskilt datum)'),
#                             ],
    periodicitet = m2m(Periodicitet,
                       null=True,
                       blank=True,
                       help_text="""Ange vid vilken tidpunkt som uppgiften lämnas in.

                       Ange vanligast förekommande om det finns variationer i tidpunkter.

                       Välj ett av värdena i listan. Vid t ex årlig uppgift, ange när på året.""")

    handelsestyrt = intf("Händelsestyrt",
                         blank=True,
                         null=True,
                         help_text="""Ange om uppgiften lämnas in utifrån händelse.""",
                         choices=JANEJ)


    MYNDIGHETSINITIERAT=1
    FORETAGSINITIERAT=2
    INITIERANDE = [(MYNDIGHETSINITIERAT, "Myndighetsinitierat"),
                   (FORETAGSINITIERAT, "Företagsinitierat")]
    initierande_part = intf(choices=INITIERANDE,
                            blank=True,
                            null=True,
                            help_text="""Ange om myndigheten eller företaget 
                          initierar uppgiftskravet första gången.""")

    ovrigt_nar = tf("Övrigt (När)",
                    blank=True,
                    help_text="""Ange eventuella övriga upplysningar - relevanta för kartläggningen
                    - som rör när uppgiftslämnande sker.""")

    beror_bransch = intf("Berör specifik bransch",
                         blank=True,
                         null=True,
                         choices=JANEJ)

    bransch = m2m(Bransch,
                  null=True,
                  blank=True,
                  help_text="""Om uppgiftskravet endast berör specifik bransch, ange den/dessa på
                  den översta nivån av SNI2007.""",
                  validators=[not_empty_list])

    arbetsgivare = intf(help_text="""Ange om uppgiftskravet endast berör arbetsgivare.""",
                        blank=True,
                        null=True,
                        choices=JANEJ)

    antal_anstallda = intf("Antal anställda",
                           help_text="Ange om uppgiftskravet endast berör företag som har ett visst antal anställda.",
                           null=True,
                           blank=True,
                           choices=JANEJ)
    
    anstallda = cf("Anställda",
                   default="",
                   blank=True,
                   max_length=100,
                   help_text="Ange svaret med större än, mindre än- och likhetstecken följt av siffra > x < y = 200")

    beror_foretagsform = intf("Berör specifika företagsformer",
                              blank=True,
                              null=True,
                              choices=JANEJ)

    foretagsform = m2m(Foretagsform,
                       null=True,
                       blank=True,
                       help_text="""Om uppgiftskravet endast berör specifika företagsformer, ange
                       dessa.""")

    storlek = intf(blank=True,
                   null=True,
                   help_text="""Ange om uppgiftskravet endast berör företag eller produktion av viss storlek.""",
                   choices=JANEJ)


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
                         help_text="""Antal olika näringsidkare/företag som har
                             haft ärenden hos myndigheten under 2012
                             till följd av uppgiftskravet.

                             Ombud avses inte.

                             Skriv svaret med siffror i cellen.""")

    annan_ingivare = intf(help_text="""Ange om uppgifter som rör uppgiftskravet kan lämnas av ombud för
                         företaget (alltså någon som
                         har fullmakt och inte är anställd).""",
                          blank=True,
                          null=True,
                          choices=JANEJ)
    
    underskrift = intf(null=True,
                       blank=True,
                       help_text="Kräver uppgiftsinlämningen underskrift (på papper eller elektroniskt)?",
                       choices=JANEJ)

    etjanst = intf("E-tjänst",
                   help_text="""Har ni en e-tjänst som kan användas för insamling av uppgiftskravet
                  (dvs tjänst som möjliggör automatiserad behandling
                  av uppgifterna)?  Här avses inte t ex
                  pdf-blankett som måste skrivas ut.""",
                   blank=True,
                   null=True,
                   choices=JANEJ)

    blankett = intf("Elektronisk blankett",
                    blank=True,
                    null=True,
                    help_text="Har ni en elektronisk blankett (t ex PDF-blankett) som kan fyllas i och lämnas in med brev, fax, e-post?",
                    choices=JANEJ)

    maskintillmaskin = intf("Maskin-till-maskingränssnitt",
                            blank=True,
                            null=True,
                            help_text="Har ni ett maskin-till-maskingränssnitt"
                            " som kan användas för insamling av uppgifter i "
                            "uppgiftskravet?",
                            choices=JANEJ)

    ENDAST_ETJANST = 0
    INGEN_INFO_TILLGANGLIG = 1
    INFO_TILLGANGLIG = 2
    BLANKETT_TILLGANGLIG = 3
    SMART_BLANKETT_TILLGANGLIG = 4
    svarighet_ej_etjanst = intf("Uppskattad svårighet att lämna uppgiftskravet - ej e-tjänst",
                                null=True,
                                blank=True,
                                choices=((ENDAST_ETJANST, "Uppgiftskravet kan endast fullgöras med e-tjänst"),
                                         (INGEN_INFO_TILLGANGLIG, "Ingen information om uppgiftskravet tillgänglig på myndighetens webbplats/er."),
                                         (INFO_TILLGANGLIG, "Information om uppgiftskravet tillgänglig på myndighetens webbplats/er."),
                                         (BLANKETT_TILLGANGLIG, "Blankett tillgänglig."),
                                         (SMART_BLANKETT_TILLGANGLIG, "Interaktiv/smart blankett tillgänglig.")),
                                help_text="""0 Uppgiftskravet kan endast fullgöras
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
    
#    lank_till_blankett = url("Länk till blankett",
#                             max_length=1000,
#                             blank=True,
#                             null=True,
#                             help_text="""Ange länk direkt till blankett i det fall det finns, annars lämna tomt.""")

    ETJANST = 5
    MASKIN_TILL_MASKIN = 6
    EJ_ETJANST = 7
    svarighet_etjanst = intf("Uppskattad svårighet att lämna uppgiftskravet - e-tjänst",
                             null=True,
                             blank=True,
                             choices=((ETJANST,"E-tjänst"),
                                      (MASKIN_TILL_MASKIN, "Maskin-till-maskin"),
                                      (EJ_ETJANST, "Ej e-tjänst")),
                             help_text="""5 E-tjänst
                          Företaget kan interaktivt navigera, vägledas, ange uppgifter
                          och lämna in online med kvittens. 

                          6 Maskin-till-maskin
                          Företaget kan ansluta ett system till ett maskingränssnitt för att lämna in uppgifter.
            
                          7 Ej e-tjänst
                          Uppgifter i uppgiftskravet kan inte samlas in via e-tjänst.
                          
                          Välj ett av värdena i listan""")

#    lank_till_etjanst = url("Länk till e-tjänst",
#                            blank=True,
#                            null=True,
#                            help_text="Ange länk till e-tjänst i det fall det finns, annars lämna tomt.")

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

    aktivt = intf("Publicerat",
                  choices=JANEJ,
                  default=NEJ,
                  help_text="""Är uppgiftskravet aktuellt, gällande och fullständigt (inte under redigering)?""")
    uppgifter = models.ManyToManyField(Uppgift, blank=True, validators=[not_empty_list])

    avgransad = bf("Avgränsat", default=False, help_text="Avgränsat enligt villkor i anvisningarnas stycke om avgränsning.")
                   

    def __unicode__(self):
        return "%s: %s" % (self.kravid, self.namn)

    def __iter__(self):
        # FIXME: This method is a clear sign that i do not know what
        # i'm doing.
        for i in self._meta.get_all_field_names():
            try:
                yield (self._meta.get_field(i), getattr(self, i))
            # meta.get_all_field_names returns "ansvarig_myndighet_id"
            # and others
            except FieldDoesNotExist:
                pass

    def natural_key(self):
        return (self.kravid,)

    def get_absolute_url(self):
        return reverse('register:krav-detail', args=[self.kravid])


    def valid(self):
        try:
            self.full_clean()
            self._basic_validation()
            return True
        except ValidationError:
            return False
    valid.boolean = True
    valid.short_description = "Fullständigt"


    def _basic_validation(self, errors=None):
        if not errors:
            errors = {}
        if not self.namn:
            errors['namn'] = ['Benämning på uppgiftskravet måste anges']
        if not self.ansvarig_myndighet:
            errors['ansvarig_myndighet'] = ['Ansvarig myndighet måste anges']
        if not self.kartlaggande_myndighet:
            errors['kartlaggande_myndighet'] = ['Kartläggande myndighet måste anges']
        if not self.lagrum:
            errors['lagrum'] = ['Författningsstöd måste anges']
        if not self.kortbeskrivning:
            errors['kortbeskrivning'] = ['Kort beskrivning av uppgiftskravet måste anges']
        if self.leder_till_insamling is None:
            errors['leder_till_insamling'] = ['Inte angivet om kravet leder till insamling från företag']
        if self.kalenderstyrt is None:
            errors['kalenderstyrt'] = ['Inte angivet om kravet är kalenderstyrt eller inte']
        if self.kalenderstyrt == Krav.JA and not self.periodicitet.count():
            errors['periodicitet'] = ['Ingen tidpunkt för inlämnande angivet även fast kravet är kalenderstyrt']
        if not self.initierande_part:
            errors['initierande_part'] = ['Initierande part ej angiven']
        if self.beror_bransch is None:
            errors['beror_bransch'] = ['Inte angivet om kravet berör någon specifik bransch']
        if self.beror_bransch == Krav.JA and not self.bransch.count():
            errors['bransch'] = ['Inga branscher angivna även fast kravet beror på detta']
        if self.arbetsgivare is None:
            errors['arbetsgivare'] = ['Inte angivet om kravet endast berör arbetsgivare']
        if self.beror_foretagsform is None:
            errors['beror_foretagsform'] = ['Inte angivet om kravet beror någon specifik företagsform']
        if self.beror_foretagsform == Krav.JA and not self.foretagsform.count():
            errors['foretagsform'] = ['Inga företagsformer angivna även fast kravet beror på detta']
        if self.annan_ingivare is None:
            errors['annan_ingivare'] = ['Inte angivet om uppgifter kan lämnas av ombud för företaget']
        if self.blankett is None:
            errors['blankett'] = ['Inte angivet om elektronisk blankett finns']
        if self.blankett == Krav.JA and not self.blanketturl_set.count():
            errors['blankett'] = ['Elektronisk blankett finns, men ingen länk till sådan är angiven']
        if self.etjanst is None:
            errors['etjanst'] = ['Inte angivet om etjänst finns']
        if self.etjanst == Krav.JA and not self.etjansturl_set.count():
            errors['etjanst'] = ['Etjänst finns, men ingen länk till sådan är angiven']
        if self.maskintillmaskin is None:
            errors['maskintillmaskin'] = ['Inte angivet om maskin-till-maskingränssnitt finns']
        
        if errors:
            raise ValidationError(errors)

    class Meta():
        verbose_name_plural = "Krav"
        ordering = ["id"]
    

# these two models shoud not have managers, or any entries in admin or
# similar -- they're just a way to have Krav.lank_till_blankett and
# Krav.lank_till_etjanst supporting multiple URLs
class BlankettURL(models.Model):
    url = models.URLField()
    krav = models.ForeignKey(Krav)
    class Meta():
        verbose_name = "Blankettlänk"
        verbose_name_plural = "Blankettlänkar"

class EtjanstURL(models.Model):
    url = models.URLField()
    krav = models.ForeignKey(Krav)
    class Meta():
        verbose_name = "Etjänstlänk"
        verbose_name_plural = "Etjänstlänkar"
