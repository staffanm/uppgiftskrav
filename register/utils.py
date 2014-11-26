# -*- coding: utf-8 -*-
def parse_lagrum(s):
    """

    >>> pprint(parse_lagrum("SFS 2008:145 3 3"))
    [{'fs': 'SFS', 'fsnr': '2008:145', 'kap': '3', 'par': '3'}]
    >>> pprint(parse_lagrum("SFS1991:1047 12"))
    [{'fs': 'SFS', 'fsnr': '1991:1047', 'par': '12'}]
    >>> pprint(parse_lagrum("SFS1995:239 11 5; SFS1995:239 11 7; SFS1995:239 7 19; SFS1995:239 7 20"))
    [{'fs': 'SFS', 'fsnr': '1995:239', 'kap': '11', 'par': '5'},
     {'fs': 'SFS', 'fsnr': '1995:239', 'kap': '11', 'par': '7'},
     {'fs': 'SFS', 'fsnr': '1995:239', 'kap': '7', 'par': '19'},
     {'fs': 'SFS', 'fsnr': '1995:239', 'kap': '7', 'par': '20'}]
    >>> pprint(parse_lagrum("SFS2010:110\\n14; SFS2010:110 31"))
    [{'fs': 'SFS', 'fsnr': '2010:110', 'par': '14'},
     {'fs': 'SFS', 'fsnr': '2010:110', 'par': '31'}]
    >>> pprint(parse_lagrum("SFS1994:200 8a 15; SFS1994:200 8a 16"))
    [{'fs': 'SFS', 'fsnr': '1994:200', 'kap': '8 a', 'par': '15'},
     {'fs': 'SFS', 'fsnr': '1994:200', 'kap': '8 a', 'par': '16'}]
    >>> pprint(parse_lagrum("SFS2000:630 39a"))
    [{'fs': 'SFS', 'fsnr': '2000:630', 'par': '39 a'}]
    >>> pprint(parse_lagrum("SFS2010:110 21  2"))
    [{'fs': 'SFS', 'fsnr': '2010:110', 'kap': '21', 'par': '2'}]
    >>> pprint(parse_lagrum("SFS2005:551 13 27;SFS2005:559 1 14;SFS2005:559 1 15"))
    [{'fs': 'SFS', 'fsnr': '2005:551', 'kap': '13', 'par': '27'},
     {'fs': 'SFS', 'fsnr': '2005:559', 'kap': '1', 'par': '14'},
     {'fs': 'SFS', 'fsnr': '2005:559', 'kap': '1', 'par': '15'}]
    >>> pprint(parse_lagrum("SFS2005:551 9 23 a"))
    [{'fs': 'SFS', 'fsnr': '2005:551', 'kap': '9', 'par': '23 a'}]
    >>> pprint(parse_lagrum("SJVFS 1995:74 2§"))
    [{'fs': 'SJVFS', 'fsnr': '1995:74', 'par': '2'}]
    >>> pprint(parse_lagrum("SJVFS 1995:162 4§ 2st"))
    [{'fs': 'SJVFS', 'fsnr': '1995:162', 'par': '4'}]
    >>> pprint(parse_lagrum("SJVFS 2005:12 ????"))
    [{'fs': 'SJVFS', 'fsnr': '2005:12'}]
    >>> pprint(parse_lagrum("SJVFS 1998:88 3 a; SJVFS 1998:88 3b"))
    [{'fs': 'SJVFS', 'fsnr': '1998:88', 'par': '3 a'},
     {'fs': 'SJVFS', 'fsnr': '1998:88', 'par': '3 b'}]
    >>> pprint(parse_lagrum("31993R2454 37;   \\n31993R2454 30A;\\nTFS2000:20 B"))
    [{'doktyp': 'R', 'year': '1993', 'ynr' '2454', 'zart': '37'},
     {'doktyp': 'R', 'year': '1993', 'ynr' '2454', 'zart': '30 a'},
     {'fs': 'TFS', 'fsnr': '2000:20'}]
    >>> pprint(parse_lagrum("31993R2454 67;\\nTFS1994:54 4 2-3"))  # '2-3' is not easily handled
    [{'doktyp': 'R', 'year': '1993', 'ynr' '2454', 'zart': '67'},
     {'fs': 'TFS', 'fsnr': '1994:54', 'kap': '4', 'par': '2'},
     {'fs': 'TFS', 'fsnr': '1994:54', 'kap': '4', 'par': '3'}]
    >>> pprint(parse_lagrum("SCB-FS2012:6 3"))
    [{'fs': 'SCB-FS', 'fsnr': '2012:6', 'par': '3'}]
    >>> #
    >>> # handling of invalid values
    >>> #
    >>> parse_lagrum("LOU2007:1091 11") # nonsensical, should be smth like "SFS2007:1091 9 1"
    []
    >>> parse_lagrum("SFS:1981:774 2; 1 SFS:1981:981 2 2") # note misplaced semicolon, should throw exception
    []
    >>> parse_lagrum("SFS1987:667 11 13 3") # what?
    [{'fsnr': '1987:667', 'par': '13 ', 'fs': 'SFS', 'kap': '11'}]
    >>> parse_lagrum("Bestämmelsen har upphört i och med SJVFS 2009:83") # well then it should be removed?
    []  
    """
    res = []
    for ref in s.split(";"):
        ref = ref.strip()
        # now you've got two problems
        m = re.match(
            '(?P<fs>[A-ZÅÄÖ\-]*FS)\s*(?P<fsnr>\d{4}:\d+)\s+((?P<kap>\d+(?:\s*[a-h]|))\s+|)(?P<par>\d+\s*[abcd]?)(?P<rest>.*)$', ref)
        if not m:
            # looser regex, matches only FS
            m = re.match(
                '(?P<fs>[A-ZÅÄÖ\-]*FS)\s*(?P<fsnr>\d{4}:\d+)(?P<rest>.*)$', ref)
            if not m:
                # eurlex regex
                m = re.match(
                    '3(?P<year>\d{4})(?P<doktyp>R)(?P<ynr>\d+)(\s+(?P<zart>\d+(\s?[A-Ha-h]?|))|)(?P<rest>.*)$', ref)
                # if m:
                #    from pdb import set_trace; set_trace()
        if m:
            # filter out named groups that has None for value
            res.append(dict([(k, v) for (k, v) in m.groupdict().items() if v]))
            if 'rest' in res[-1]:
                # print("WARNING: Couldn't understand tail %r on %r" % (res[-1]['rest'], ref))
                del res[-1]['rest']
            # canonicalize "18a" => "18 a"
            for fld in ('kap', 'par', 'zart'):
                if fld not in res[-1]:
                    continue
                groups = re.match(
                    "(\d+)(?: *([A-Ha-h])|)", res[-1][fld]).groups()
                if groups[1]:
                    # print("Groups b4 lc:" + repr(groups))
                    groups = tuple([x.lower() for x in groups])
                    # print("Groups after lc:" + repr(groups))
                    res[-1][fld] = "%s %s" % groups
    return res


def format_lagrum(*lagrum):
    """
    >>> format_lagrum({'fs': 'SFS', 'fsnr': '2008:145', 'kap': '3', 'par': '3'})
    ("3 kap. 3 § lagen (2008:145) om statligt tandvårdsstöd",)
    """
    return ("3 kap. 3 § lagen (2008:145) om statligt tandvårdsstöd", )

def format_link(*lagrum):
    for parts in lagrum:
        # eg http://www.riksdagen.se/sv/Dokument-Lagar/Lagar/Svenskforfattningssamling/-_sfs-1998-204/#P5
        if 'fs' in parts and parts['fs'] == 'SFS':
            frag = "P%s" % parts['par'].replace(" ", "")
            if 'kap' in parts:
                frag = ("K%s" % (parts['kap'].replace(" ", ""))) + frag
            yield ("http://www.riksdagen.se/sv/Dokument-Lagar/Lagar/Svenskforfattningssamling/-_sfs-%s/%s" %
                   parts['fsnr'].replace(":", "-"))
        else:
            yield None
