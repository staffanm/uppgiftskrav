import sys
from openpyxl import load_workbook

def myndighet_id(d,key):
    if not key in d:
        d[key] = {'id': len(d)+1}
    return d['id']



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: %s [new excel data] [old excel data] [fixture]" % sys.argv[0])
        sys.exit()

    newdata = sys.argv[1]
    olddata = sys.argv[2]
    fixture = sys.argv[3]
    ws = load_workbook(newdata).get_active_sheet()

    # these could be set dynamically by examining ws.rows[0]
    ID = 3
    MYNDIGHET = 2
    NAMN = 4
    BESKRIVNING = 9
    LAGRUM = 7

    krav = {}
    uppgift = {}
    myndighet = {}
    
    for (cnt, row) in enumerate(ws.rows[1:]):
        cnt += 1
        krav[row[ID].value] = {'id': cnt, 
                               'kravid': row[ID].value,
                               'namn': row[NAMN].value,
                               'beskrivning': row[BESKRIVNING].value[:10],
                               'lagrum': row[LAGRUM].value,
                               'myndighet': myndighet_id(myndighet, 
                                                         row[MYNDIGHET].value)
                 }
    pprint(uppgift)
    ws = load_workbook(olddata).get_active_sheet()
    for (cnt, cell) in enumerate(ws.rows[0][30:]):
        uppgift[cnt] = {'id': cnt,
                        'uppgiftid': 'UD%04d'% cnt,
                        'namn': cell.value}
    for row in ws.rows[1:]:
        kravid = row[ID].value
        d = krav[kravid]
        d['uppgifter'] = [cnt for (cnt, x) in enumerate(row[30:]) if x.value in ('Obligatorisk', 'Frivillig')]
        
        

                                     
