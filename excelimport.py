#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
from collections import OrderedDict
import sys
from openpyxl import load_workbook
from pprint import pprint
import json

def myndighet_id(d,key):
    assert key
    if not key in d:
        d[key] = {'id': len(d)+1,
                  'name': key}
    return d[key]['id']

def make_fixture(newdata, olddata, fixture):
    # 1: Extract all Kravs (and create a list of Myndigheter as 
    # django.contrib.auth.models.Group as well)
    print("Opening new data %s" % newdata)
    ws = load_workbook(newdata, use_iterators=True).get_active_sheet()

    # these could be set dynamically by examining ws.rows[0]
    ID = 3
    MYNDIGHET = 2
    NAMN = 4
    BESKRIVNING = 9
    LAGRUM = 7

    krav = OrderedDict()
    uppgift = OrderedDict()
    myndighet = OrderedDict()
    myndighet['Företagsdatanämnden'] = {'id': 1,
                                        'name': 'Företagsdatanämnden'}
    print("Enumerating Krav")
    for (cnt, row) in enumerate(ws.iter_rows()):
        if cnt < 1 or not row[MYNDIGHET].internal_value:
            continue
        try:
            beskrivning = row[BESKRIVNING].internal_value
            if not beskrivning:
                beskrivning = '[Beskrivning saknas]'

        except TypeError: # empty (NoneType) cell
            beskrivning = '[Beskrivning saknas]'

        lagrum = row[LAGRUM].internal_value
        if not lagrum:
            lagrum = "[lagrum saknas]"
            
        krav[row[ID].internal_value] = {'id': cnt, 
                               'kravid': row[ID].internal_value,
                               'namn': row[NAMN].internal_value,
                               'beskrivning': beskrivning,
                               'lagrum': lagrum.strip()[:255],
                               'myndighet': myndighet_id(myndighet, 
                                                         row[MYNDIGHET].internal_value),
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
    data = []
    for m in myndighet.values():
        data.append({'model': 'auth.group', # 'django.contrib.auth.models.Group',
                     'pk': m['id'],
                     'fields': {'name': m['name'],
                                'permissions': []}
                     })
                            
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
        ck['url'] = '' # not currently extracted from excel data
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
