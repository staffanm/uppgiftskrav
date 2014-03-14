#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from collections import OrderedDict
import json
import re
import sys

from openpyxl import load_workbook

assert sys.version_info < (3,0,0), "String handling not Py3 compliant, plz rewrite"

def myndighet_id(d,key):
    assert key
    if not key in d:
        d[key] = {'id': len(d)+1,
                  'name': key}
    return d[key]['id']

def value(row, idx, max_length=None):
    val = row[idx].internal_value
    if isinstance(val, float):
        return unicode(int(val)) # 0.0 -> '0'
    elif not val:
        return ""
    if not isinstance(val, unicode):
        val = unicode(val)
    if max_length:
        val = val[:max_length]
    return val.strip()

    
def note(row, idx, dictionary):
    val = value(row, idx)
    if val not in dictionary and val:
        dictionary[val] = len(dictionary)+1
    return val

def choice(row, idx, choices, default=None):
    val = value(row, idx)
    lval = val.lower()
    lchoices = [x.lower() if hasattr(x,'lower') else x for x in choices ]
    if lval in lchoices:
        return lchoices.index(lval)
    else:
        if val:
            print("WARNING (%s): %r not in %r" %(row[3].internal_value, val, choices))
        if default is not None: # must be able to be 0 or other falsieness
            return default
        else:
            raise KeyError(val)

def integer(row, idx):
    val = value(row, idx)
    if val and val.isdigit():
        return int(val)
    # else return None

def nbf(row, idx):
    return choice(row, idx, ('Nej', 'Ja'), -1)
    #val = value(row, idx)
    #if val:
    #    return val == "Ja"
    #else:
    #    return None

def many(row, idx):
    val = value(row, idx)
    if val:
        l = val.split(",")
        return [[x.strip().upper()] for x in l if x.strip()]
    else:
        return []
        
def make_fixture(newdata, olddata, fixture):
    # 1: Extract all Kravs (and create a list of Myndigheter as 
    # django.contrib.auth.models.Group as well)
    print("Opening new data %s" % newdata)
    ws = load_workbook(newdata, use_iterators=True).get_active_sheet()

    # these could be set dynamically by examining ws.rows[0]
    VERKSAMHETSOMRADE = 0
    ANSVARIG_MYNDIGHET = 1
    KARTLAGGANDE_MYNDIGHET = 2
    ID = 3
    NAMN = 4 # UPPGIFTSKRAV
    FORFATTNING = 5 # deprecated
    PARAGRAF = 6 # deprecated
    LAGRUM = 7
    URSPRUNG = 8
    BESKRIVNING = 9 # deprecated 
    ANTECKNING = 10
    KORT_BESKRIVNING = 11
    LEDER_TILL_INSAMLING = 12
    EGNA_NOTERINGAR = 13
    KALENDERSTYRT = 14
    PERIODICITET = 15
    HANDELSESTYRT = 16
    INITIERANDE_PART = 17
    OVRIGT_NAR = 18
    BRANSCH = 19
    ARBETSGIVARE = 20
    FORETAGSFORM = 21
    STORLEK = 22
    STORLEKSKRITERIER = 23
    OVRIGA_URVALSKRITERIER = 24
    ANTAL_FORETAG = 25
    ANNAN_INGIVARE = 26
    UNDERSKRIFT = 27
    ETJANST = 28
    SVARIGHET_EJ_ETJANST = 29
    SVARIGHET_ETJANST = 30
    VOLYMER_TIDIGARE = 31
    VOLYMER_2012 = 32
    VOLYMER_ETJANST = 33
    OVRIGT_HUR = 34

    krav = OrderedDict()
    uppgift = OrderedDict()
    verksamhetsomrade = OrderedDict()
    myndighet = OrderedDict()
    myndighet['Företagsdatanämnden'] = 1

    print("Enumerating Krav")
    for (cnt, row) in enumerate(ws.iter_rows()):
        if cnt < 1 or not row[ID].internal_value:
            continue
        
        krav[row[ID].internal_value] = {'id': cnt,
                                        'kravid': value(row, ID, max_length=7),
                                        'verksamhetsomrade': [note(row, VERKSAMHETSOMRADE, verksamhetsomrade)],
                                        'ansvarig_myndighet': [note(row, ANSVARIG_MYNDIGHET, myndighet)],
                                        'kartlaggande_myndighet': [note(row, KARTLAGGANDE_MYNDIGHET, myndighet)],
                                        'namn': value(row, NAMN),
                                        'forfattning': value(row, FORFATTNING, max_length=50),
                                        'paragraf': value(row, PARAGRAF, max_length=50),
                                        'lagrum': value(row, LAGRUM, max_length=255),
                                        'ursprung': choice(row, URSPRUNG, (False, "Nationellt", "EU mm"), default=-1),
                                        'beskrivning': value(row, BESKRIVNING),
                                        'anteckning': value(row, ANTECKNING),
                                        'kortbeskrivning': value(row, KORT_BESKRIVNING),
                                        'leder_till_insamling': nbf(row, LEDER_TILL_INSAMLING),
                                        'egna_noteringar': value(row, EGNA_NOTERINGAR),
                                        'kalenderstyrt': nbf(row, KALENDERSTYRT),
                                        'periodicitet': choice(row, PERIODICITET, ('Inte relevant', 'Januari', 'Februari', 'Mars', 'April', 'Maj', 'Juni', 'Juli', 'Augusti', 'September', 'Oktober', 'November', 'December', 'Veckovis', 'Månadsvis', 'Kvartalsvis', 'Årsvis (ej särskilt datum)'), default=-1),
                                        'handelsestyrt': nbf(row, HANDELSESTYRT),
                                        'initierande_part': choice(row, INITIERANDE_PART, (False, 'Myndigheten', 'Företaget', 'Båda'), default=-1),
                                        'ovrigt_nar': value(row, OVRIGT_NAR),
                                        'bransch': many(row, BRANSCH),
                                        'arbetsgivare': nbf(row, ARBETSGIVARE),
                                        'foretagsform': many(row, FORETAGSFORM),
                                        'storlek': nbf(row, STORLEK),
                                        'storlekskriterier': value(row, STORLEKSKRITERIER),
                                        'ovriga_urvalskriterier': value(row, OVRIGA_URVALSKRITERIER),
                                        'antal_foretag': integer(row, ANTAL_FORETAG),
                                        'annan_ingivare': nbf(row, ANNAN_INGIVARE),
                                        'underskrift': nbf(row, UNDERSKRIFT),
                                        'etjanst': nbf(row, ETJANST),
                                        'svarighet_ej_etjanst': choice(row, SVARIGHET_EJ_ETJANST, ('0','1','2','3','4'), default=-1),
                                        'svarighet_etjanst': choice(row, SVARIGHET_ETJANST, (False, False, False, False, False, '5','6','7'), default=-1),
                                        'volymer_tidigare': integer(row, VOLYMER_TIDIGARE),
                                        'volymer_2012': integer(row, VOLYMER_2012),
                                        'volymer_etjanst': integer(row, VOLYMER_ETJANST),
                                        'ovrigt_hur': value(row, OVRIGT_HUR),
                                        'uppgifter': []
                           }
        sys.stdout.write(".")
        sys.stdout.flush()
    print("\nDone, %s krav (%s myndigheter) in %s" % (len(krav), len(myndighet), newdata))

    # 2: Find information about Grundläggande uppgifter (GU)
    print("Opening old data %s" % olddata)
    ws = load_workbook(olddata, use_iterators=True).get_active_sheet()
    print("Enumerating Uppgifter")
    rows = ws.iter_rows()
    next(rows) # 1st row contains no usable data
    firstrow = next(rows)
    for (cnt, cell) in enumerate(firstrow[30:]):
        uppgift[cnt] = {'id': cnt+1,
                        'uppgiftid': 'UD%04d' % (cnt+1),
                        'namn': cell.internal_value}

    print("Done, found %s uppgifter" % len(uppgift))

    # 3: connect each Krav to a number of GU
    print("Connecting uppgifter to krav")
    for row in rows:
        try:
            kravid = row[ID].internal_value
            d = krav[kravid]
        except KeyError:
            # quite a common problem, olddata contains 2409 rows, newdata contains 1422 rows
            # print("Old data contained krav %s which is not present in new data" % row[ID].internal_value)
            continue

        d['uppgifter'] = [cnt+1 for (cnt, x) in enumerate(row[30:]) if x.internal_value in ('Obligatorisk', 'Frivillig')]
        sys.stdout.write(".")
        sys.stdout.flush()

    print("\nDone, now reformatting to fixture format")
    # 4: reformat everything to appropriate json dicts

    # 4.1 hardcode Bransch / företagsform
    data = [{'model': 'register.bransch',
             'pk': 1,
             'fields': {'snikod': 'A',
                        'beskrivning': 'Jordbruk, skogsbruk och fiske'}},
            {'model': 'register.bransch',
             'pk': 2,
             'fields': {'snikod': 'B', 
                        'beskrivning': 'Utvinning av mineral'}},
            {'model': 'register.bransch',
             'pk': 3,
             'fields': {'snikod': 'C', 
                         'beskrivning': 'Tillverkning'}},
            {'model': 'register.bransch',
             'pk': 4,
             'fields': {'snikod': 'D', 
                        'beskrivning': 'Försörjning av el, gas, värme och kyla'}},
            {'model': 'register.bransch',
             'pk': 5,
             'fields': {'snikod': 'E', 
                        'beskrivning': 'Vattenförsörjning; avloppsrening, avfallshantering och sanering'}},
            {'model': 'register.bransch',
             'pk': 6,
             'fields': {'snikod': 'F', 
                        'beskrivning': 'Byggverksamhet'}},
            {'model': 'register.bransch',
             'pk': 7,
             'fields': {'snikod': 'G', 
                        'beskrivning': 'Handel; reparation av motorfordon och motorcyklar'}},
            {'model': 'register.bransch',
             'pk': 8,
             'fields': {'snikod': 'H', 
                        'beskrivning': 'Transport och magasinering'}},
            {'model': 'register.bransch',
             'pk': 9,
             'fields': {'snikod': 'I', 
                        'beskrivning': 'Hotell- och restaurangverksamhet'}},
            {'model': 'register.bransch',
             'pk': 10,
             'fields': {'snikod': 'J', 
                        'beskrivning': 'Informations- och kommunikationsverksamhet'}},
            {'model': 'register.bransch',
             'pk': 11,
             'fields': {'snikod': 'K', 
                        'beskrivning': 'Finans- och försäkringsverksamhet'}},
            {'model': 'register.bransch',
             'pk': 12,
             'fields': {'snikod': 'L', 
                        'beskrivning': 'Fastighetsverksamhet'}},
            {'model': 'register.bransch',
             'pk': 13,
             'fields': {'snikod': 'M', 
                        'beskrivning': 'Verksamhet inom juridik, ekonomi, vetenskap och teknik'}},
            {'model': 'register.bransch',
             'pk': 14,
             'fields': {'snikod': 'N', 
                        'beskrivning': 'Uthyrning, fastighetsservice, resetjänster och andra stödtjänster'}},
            {'model': 'register.bransch',
             'pk': 15,
             'fields': {'snikod': 'O', 
                        'beskrivning': 'Offentlig förvaltning och försvar; obligatorisk socialförsäkring'}},
            {'model': 'register.bransch',
             'pk': 16,
             'fields': {'snikod': 'P', 
                        'beskrivning': 'Utbildning'}},
            {'model': 'register.bransch',
             'pk': 17,
             'fields': {'snikod': 'Q', 
                        'beskrivning': 'Vård och omsorg; sociala tjänster'}},
            {'model': 'register.bransch',
             'pk': 18,
             'fields': {'snikod': 'R', 
                        'beskrivning': 'Kultur, nöje och fritid'}},
            {'model': 'register.bransch',
             'pk': 19,
             'fields': {'snikod': 'S', 
                        'beskrivning': 'Annan serviceverksamhet'}},
            {'model': 'register.bransch',
             'pk': 20,
             'fields': {'snikod': 'T', 
                        'beskrivning': 'Förvärvsarbete i hushåll; hushållens produktion av diverse varor och tjänster för eget bruk'}},
            {'model': 'register.bransch',
             'pk': 21,
             'fields': {'snikod': 'U', 
                        'beskrivning': 'Verksamhet vid internationella organisationer, utländska ambassader o.d.'}},
            {'model': 'register.bransch',
             'pk': 22,
             'fields': {'snikod': 'X', 
                        'beskrivning': 'Avser alla'}},
            {'model': 'register.foretagsform',
             'pk': 1,
             'fields': {'formkod': 'E', 
                        'beskrivning': 'Enskild näringsidkare'}},
            {'model': 'register.foretagsform',
             'pk': 2,
             'fields': {'formkod': 'AB', 
                        'beskrivning': 'Aktiebolag'}},
            {'model': 'register.foretagsform',
             'pk': 3,
             'fields': {'formkod': 'HB', 
                        'beskrivning': 'Handelsbolag'}},
            {'model': 'register.foretagsform',
             'pk': 4,
             'fields': {'formkod': 'KB', 
                        'beskrivning': 'Kommanditbolag'}},
            {'model': 'register.foretagsform',
             'pk': 5,
             'fields': {'formkod': 'BRF', 
                        'beskrivning': 'Bostadsrättsförening'}},
            {'model': 'register.foretagsform',
             'pk': 6,
             'fields': {'formkod': 'EK', 
                        'beskrivning': 'Ekonomisk förening'}},
            {'model': 'register.foretagsform',
             'pk': 7,
             'fields': {'formkod': 'A', 
                        'beskrivning': 'Annan företagsform'}},
            {'model': 'register.foretagsform',
             'pk': 8,
             'fields': {'formkod': 'X', 
                        'beskrivning': 'Avser alla'}},
            ]
    
    # 4.2 the rest
    for name, id in myndighet.items():
        data.append({'model': 'auth.group', # 'django.contrib.auth.models.Group',
                     'pk': id, 
                     'fields': {'name': name,
                                'permissions': [["add_krav", "register", "krav"],
                                                ["change_krav", "register", "krav"],
                                                ["delete_krav", "register", "krav"],
                                                ["add_verksamhetsomrade", "register", "verksamhetsomrade"],
                                                ["change_verksamhetsomrade", "register", "verksamhetsomrade"],
                                                ["delete_verksamhetsomrade", "register", "verksamhetsomrade"]]
                                            } 
                     })

    # add a user for each as well. The passwd is "test"
    names = {"Företagsdatanämnden": '',
             "Försäkringskassan": 'dan', 
             "Kronofogdemyndigheten": 'eva', 
             "Arbetsförmedlingen": 'clas', 
             "Bolagsverket": 'helena',
             "Bokföringsnämnden": 'olle',
             "Patentombudsnämnden": 'karin', 
             "Livsmedelsverket": 'stig', 
             "SCB": 'johan',
             "Medlingsinstitutet": 'claes', 
             "Statens energimyndighet": 'erik', 
             "Tillväxtanalys": 'hjalmarsson', 
             "Finansinspektionen": 'martin', 
             "Naturvårdsverket": 'maria', 
             "Skolverket": 'ekstrom', 
             "Skogsstyrelsen": 'monika', 
             "Tillväxtverket": 'anna',
             "Trafikanalys": 'brita', 
             "Trafikverket": 'gunnar', 
             "Tullverket": 'therese', 
             "Skatteverket": 'lars',
             "Transportstyrelsen": 'widlert', 
             "Jordbruksverket": 'leif'}
    for name, id in myndighet.items():
        username = names.get(name,
                             name.replace(" ","").lower())
        data.append({'model': 'auth.user',
                     'pk': id,
                     "fields": {
                         "username": username,
                         "first_name": "", 
                         "last_name": "", 
                         "is_active": True, 
                         "is_superuser": False, 
                         "is_staff": True, 
                         "last_login": "2014-02-07T13:38:58Z", 
                         "groups": [[name]], 
                         "user_permissions": [], 
                         "password": "pbkdf2_sha256$12000$jn0OqvMfv7Ys$pEaHcw+ruR7OJJL8qDa3iWC+P8Vu74fUTuD04vDHAfI=", 
                         "email": "", 
                         "date_joined": "2014-02-07T13:38:58Z"
                         }})
    # and some super users
    for (offset, name) in enumerate(('staffan', 'cecilia', 'magnus', 'maryam', 'janne', 'annika', 'bengt')):
        data.append({'model': 'auth.user',
                     'pk': len(myndighet)+offset+1,
                     "fields": {
                         "username": name,
                         "first_name": "", 
                         "last_name": "", 
                         "is_active": True, 
                         "is_superuser": True, 
                         "is_staff": True, 
                         "last_login": "2014-02-07T13:38:58Z", 
                         "groups": [], 
                         "user_permissions": [], 
                         "password": "pbkdf2_sha256$12000$jn0OqvMfv7Ys$pEaHcw+ruR7OJJL8qDa3iWC+P8Vu74fUTuD04vDHAfI=", 
                         "email": "", 
                         "date_joined": "2014-02-07T13:38:58Z"
                         }})
        
    for name, id in verksamhetsomrade.items():
        data.append({'model': 'register.verksamhetsomrade',
                     'pk': id,
                     'fields': {'omrade': name}})

    for u in uppgift.values():
        data.append({'model': 'register.uppgift',
                     'pk': u['id'],
                     'fields': {'uppgiftid': u['uppgiftid'],
                                'namn': u['namn']}
                     })

    for k in krav.values():
        ck = k.copy()
        del ck['id']
        # ck['myndighet']
        # ck['uppgifter']
        # ck['url'] = '' # not currently extracted from excel data
        data.append({'model': 'register.krav',
                     'pk': k['id'],
                     'fields': ck
                     })
        
    # 5: aaaand we're done
    print("Serializing to JSON as %s" % fixture)
    with open(fixture, "w") as fp:
        json.dump(data, fp, indent=4)
    print("Wrote %s entries to %s" % (len(data), fixture))

if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: %s [new excel data] [old excel data] [fixture]" % sys.argv[0])
        sys.exit()

    newdata = sys.argv[1]
    olddata = sys.argv[2]
    fixture = sys.argv[3]
    make_fixture(newdata, olddata, fixture)
