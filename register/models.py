from django.db import models
from django.contrib.auth import models as authmodels

class Uppgift(models.Model):
    uppgiftid = models.CharField(max_length=8)
    namn = models.CharField(max_length=100)
    # ...

    def __unicode__(self):
        return "%s: %s" % (self.uppgiftid, self.namn)

class Krav(models.Model):
    kravid = models.CharField(max_length=6)
    namn = models.CharField(max_length=100)
    beskrivning = models.TextField()
    lagrum = models.CharField(max_length=60)
    url = models.URLField()
    uppgifter = models.ManyToManyField(Uppgift)
    myndighet = models.ForeignKey(authmodels.Group)

    def __unicode__(self):
        return "%s: %s" % (self.kravid, self.namn)



    
