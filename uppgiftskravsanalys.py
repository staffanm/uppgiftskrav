#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function

CSV_ENCODING = "mac_roman"

import os, sys, csv, codecs, re
from pprint import pprint
from operator import itemgetter
from datetime import datetime
from cgi import escape
import xml.etree.cElementTree as ET
uppgiftskrav = {}

def load_csv_files(dirname):
    res = []
    for filename in os.listdir(dirname):
        if filename.endswith(b".csv"):
            print("Läser in %r" % filename)
            res.extend(load_csv(dirname+os.sep+filename))
    print("%s uppgiftskrav inlästa"%len(res))
    cnt = 0
    for krav in res:
        if krav['Leder till insamling från företag'] == 'Ja':
            cnt += 1
    print("%s uppgiftskrav leder till insamling"%cnt)
    return res

def sanitize_data(data):
    print("Filtrerar, ensar och kompletterar data")
    res = []
    namn = {}
    text = {}
    success = 0
    for row in data:
        if row['Leder till insamling från företag'] != 'Ja':
            continue

        if row['Författning']:
            # print("Analysing %r\t%r" % (row['Författning'],row['Paragraf']))
            pass

        # 1. For SFS statutes, normalize the SFS identifier and look up the name / label for the statute
        sfs = kap = par = None

        if ("FS" in row['Författning'] and not re.search(r"\bSFS",row['Författning'])):
            # print("%r är nog inte en SFS" % row['Författning'])
            pass
        else:
            m = re.search("(\d{4}:\d+)",row['Författning'])
            if m:
                sfs = m.group(1)
            else:
                # print("%r är nog inte heller en SFS" % row['Författning'])
                pass
        row['_lagrum'] = "%s %s" % (row['Författning'], row['Paragraf'])
        if sfs:
            row['_författning'] = get_label(sfs)
            # print("%s -> %s" % (row['Författning'], row['_författning']))

        # 2. Then attempt to normalize section reference
        if sfs and row['Paragraf']:
            m = re.search("(|(\d+ ?\w?) ?kap\.? )(\d+ ?\w?) ?§", row['Paragraf'])
            if m:
                kap = m.group(2)
                par = m.group(3)
                success += 1
                # print("%r -> %s kap. %s §" % (row['Paragraf'], kap, par))
            else:
                print("Svårparsad paragrafangivelse [%s]: %s" % (row['ID'], row['Paragraf']))
        

        if sfs:
            if kap:
                row['_lagrum'] = "http://rinfo.lagrummet.se/publ/sfs/%s#K%sP%s" % (sfs,kap.replace(" ",""),
                                                                                   par.replace(" ",""))
            elif par:
                row['_lagrum'] = "http://rinfo.lagrummet.se/publ/sfs/%s#P%s" % (sfs,par.replace(" ",""))
            else:
                row['_lagrum'] = "http://rinfo.lagrummet.se/publ/sfs/%s" % (sfs)
            # get html fragment of statute section text 
            # row['_författningstext'] = '<p><b>%s</b> %s' % (row['Paragraf'], get_text(sfs,row['_lagrum']))
            row['_författningstext'] = '<p>%s</p>' % (get_text(sfs,row['_lagrum']))

        else:
            if row['Författning']:
                row['_författning'] = row['Författning']
                # Attempt to separate EU legislation from local agency legislation?
                regex = "([A-ZÅÄÖ\-]+FS) ?(\d{4}:\d+)"
                if "FS" in row['Författning'] and re.search(regex,row['Författning']):
                    # print("%s är nog en föreskrift" % row['Författning'])
                    m  = re.search(regex,row['Författning'])
                    fs = m.group(1)
                    no = m.group(2)
                    row['_lagrum'] = "http://rinfo.lagrummet.se/publ/x/%s/%s" % (fs,no)
                    # row['_författningstext'] = '<p><b>%s %s</b> %s' % (row['Författning'], row['Paragraf'], '[Föreskriftstext saknas här]')
                    row['_författningstext'] = '<p>%s</p>' % ('[Föreskriftstext saknas här]')

                else:
                    # print("%s är nog EU-rätt" % row['Författning'])
                    # print("%r är nog inte heller en SFS" % row['Författning'])
                    row['_lagrum'] = "http://rinfo.lagrummet.se/publ/y/%s" % row['Författning']
                    row['_författningstext'] = '<p>%s</p>' % ('[EU-rättslig text saknas här]')
            else:
                # last resort
                row['_lagrum'] = "http://rinfo.lagrummet.se/publ/z/Unknown"
                row['_författning'] = "Okänd författning"
                row['_författningstext'] = None
        res.append(row)
    print("Efter ensning: %s författningsreferenser till SFS på paragrafnivå" % success)
    return res

sfs_namn = {}
def get_label(sfs):
    if sfs not in sfs_namn:
        path = "sfs/%s/%s.xht2" % tuple(sfs.split(":"))
        if os.path.exists(path):
            tree = ET.parse(open(path))
            label = tree.find(".//{http://www.w3.org/2002/06/xhtml2/}title").text
        else:
            label = "SFS %s" % sfs
        sfs_namn[sfs] = label
    return sfs_namn[sfs]

sfs_text = {}
def get_text(sfs, uri):
    if uri not in sfs_text:
        if "#" in uri:
            # print("Hämtar lagtext för %s" % uri)
            path = "sfs/%s/%s.xht2" % tuple(sfs.split(":"))
            if os.path.exists(path):
                about = uri[uri.index("#"):]
                tree = ET.parse(open(path))

                xpath = ".//*[@about='%s']" % about
                node = tree.find(xpath)
                if node:
                    bet = node.find("*[@class='paragrafbeteckning']")
                    if bet:
                        print("REMOVE! %s" % uri)
                        node.remove(bet)
                    text = ET.tostring(node, method="text", encoding="utf-8").decode("utf-8")
                    comment = tree.find(".//*[@property='rdfs:comment']")
                    if comment != None and "upphävd" in comment.text:
                        text = ("<b>Observera: %s</b><br/> " % comment.text) + text                        
                else:
                    text = "[Lagtexten för den angivna paragrafen %s kunde inte hittas. Upphävd?]" % about[1:]
            else:
                text = "[Lagtexten till SFS %s kunde inte hittas. Upphävd?]" % sfs
        else:
            text = "[Lagtexten återges inte här]"
        sfs_text[uri] = text
    return sfs_text[uri]
        
    
def create_html_report(data, outfile="uppgiftskrav.html"):
    print("Skapar rapport %s" % outfile)
    data = sorted(data, key=itemgetter("_lagrum"))
    cur_forfattning = None
    cur_type = None
    with codecs.open(outfile,"w",encoding="utf-8") as fp:
        fp.write("""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<title>Uppgiftskravssammanställning</title>
<style type="text/css">
@page {
    margin-top: 50pt;
    margin-bottom: 50pt;
    margin-inside: 50pt;
    margin-outside: 30pt;
    padding: 0;
}
body { column-count: 2; column-gap: 1.5em; column-fill: auto; font: 10pt/1.2 Georgia; }
h1 { color: darkslategray; font-family: Verdana ; column-span: all; font-size: 13pt }
h2 { color: darkslategray; font-family: Verdana; font-size: 11pt;}
h3 { border-top: 1px solid grey; color: darkslategray; font-family: Verdana; font-size: 10pt;}
.beskrivning { border: solid 1px black;
               margin-bottom: 6pt;
               padding: 2pt;}

.beskrivning p { padding: 0; margin: 0; }

.anteckning { border: solid 1px black;
              background-color: yellow;
              padding:0.5em;
              font-family: Comic Sans MS;
              font-size: 8pt;
              margin-bottom: 6pt;
              position:relative; }
.meta { border: solid 1px black;
        background-color: lightgray;
        margin-bottom: 6pt;
        padding: 2pt;}
.meta p { padding: 0; margin: 0; }
</style>
</head>
<body>
<h1>Uppgiftskravssammanställning</h1>
<p><em>Genererad %s</em></p>
""" % datetime.now())

        types = {'sfs':"Författningar i SFS",
                 'x':"Myndighetsföreskrifter",
                 'y':"EU-rätten",
                 'z':"Okända författningar"}

        type_cnt = 0
        for r in data:
            if r['Leder till insamling från företag'] != 'Ja':
                continue
            if cur_type != r['_lagrum'].split("/")[4]:
                if cur_type:
                    print("%s uppgiftskrav från %s" % (type_cnt,types[cur_type]))
                cur_type = r['_lagrum'].split("/")[4]
                fp.write("<h1>%s</h1>" % types[cur_type])
                type_cnt = 0
            
            type_cnt += 1
            if cur_forfattning != r['_författning']:
                cur_forfattning = r['_författning']
                fp.write("<h2>%s</h2>" % cur_forfattning)
            fp.write("<h3>%s: %s</h3>" % (r['ID'], escape(r['Informationskrav'])))
            if r['_författningstext']:
                fp.write("<div class='forfattningstext'>%s</div>" % r['_författningstext'])
            fp.write("""<div class='meta'>
                          <p><b>Ansvarig myndighet</b>:%s</p>
                          <p><b>Författning</b>:%s</p>
                          <p><b>Paragraf</b>:%s</p>
                        </div>""" % (r['Ansvarig myndighet'], r['Författning'], r['Paragraf']))
            if r['Beskrivning'] and r['Beskrivning'] != '-':
                fp.write("<div class='beskrivning'><p><b>Beskrivning</b>:%s</p></div>" % escape(r['Beskrivning']))
            if r['Anteckning']:
                fp.write("<div class='anteckning'>%s</div>" % escape(r['Anteckning']))

        fp.write("""</body></html>""")

def convert_report_to_pdf(infile="uppgiftskrav.html", outfile="uppgiftskrav.pdf"):
    print("Konverterar till %s" % outfile)
    os.system("prince %s -o %s" % (infile, outfile))

def load_csv(filename):
    csv.register_dialect("semicolon", delimiter=b';')
    # convert input stream from mac_roman to utf-8
    recoder = codecs.StreamRecoder(open(filename),
                                   codecs.getencoder('utf-8'), 
                                   codecs.getdecoder('utf-8'), 
                                   codecs.getreader(CSV_ENCODING), 
                                   codecs.getwriter(CSV_ENCODING))

    reader = csv.reader(recoder,dialect="semicolon")
    cols = None
    res = []
    for row in reader:
        # unicodize the utf-8 data provided by csv.reader
        row = [x.decode('utf-8') for x in row]
        if row[0] == 'Verksamhetsområde':
            cols = row
        elif cols:
            rowdict = dict(zip(cols,row))
            if rowdict['ID']:
                res.append(rowdict)
        else:
            pass # can't do anything until we've found the header line (typically 2nd row)
    return res

if __name__ == "__main__":
    create_html_report(sanitize_data(load_csv_files(sys.argv[1])))
    convert_report_to_pdf()
