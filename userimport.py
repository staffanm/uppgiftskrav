#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import sys
import yaml
import json
from django.conf import settings
settings.configure()
from django.contrib.auth.models import User

DEFAULT_PERMS = [["add_krav", "register", "krav"],
                 ["change_krav", "register", "krav"],
                 ["delete_krav", "register", "krav"],
                 ["add_verksamhetsomrade", "register", "verksamhetsomrade"],
                 ["change_verksamhetsomrade", "register", "verksamhetsomrade"],
                 ["delete_verksamhetsomrade", "register", "verksamhetsomrade"],
                 ["add_kravomrade", "register", "kravomrade"],
                 ["change_kravomrade", "register", "kravomrade"],
                 ["delete_kravomrade", "register", "kravomrade"],
                 ["add_blanketturl", "register", "blanketturl"],
                 ["change_blanketturl", "register", "blanketturl"],
                 ["delete_blanketturl", "register", "blanketturl"],
                 ["add_etjansturl", "register", "etjansturl"],
                 ["change_etjansturl", "register", "etjansturl"],
                 ["delete_etjansturl", "register", "etjansturl"]
        ]

def hashpwd(pwd):
    u = User()
    u.set_password(pwd)
    return u.password


def make_groups_and_users(yamlfile, fixturefile):
    # Reads information about groups and users from a given YAML file,
    # constructs a corresponding JSON fixture for those groups/users
    # and saves it in the named fixture file

    with open(yamlfile) as fp:
        indata = yaml.load(fp.read())
    outdata = []
    userpk = 0
    for (id, groupsect) in enumerate(indata):
        # 'django.contrib.auth.models.Group',
        outdata.append({'model': 'auth.group',
                        'pk': id + 1, 
                        'fields': {'name': groupsect['group'],
                                   'permissions': DEFAULT_PERMS
                               }
                    })
        superuser = groupsect['group'] == "Uppgiftslämnarutredningen"
        if not 'users' in groupsect:
            continue
        for usersect in groupsect['users']:
            assert len(usersect) == 1, "User should be specified like '- username: passwd' (got %s)" % usersect
            username, passwd = usersect.items()[0]
            userpk += 1
            outdata.append({'model': 'auth.user',
                            'pk': userpk,
                            "fields": {
                                "username": username,
                                "first_name": "",
                                "last_name": "",
                                "is_active": True,
                                "is_superuser": superuser,
                                "is_staff": True,
                                "last_login": "2014-02-07T13:38:58Z",
                                "groups": [[groupsect['group']]],
                                "user_permissions": [],
                                "password": hashpwd(passwd),
                                "email": "",
                                "date_joined": "2014-02-07T13:38:58Z"
                            }})
    with open(fixturefile, "w") as fp:
        json.dump(outdata, fp, indent=4)
    print("Dumped %s entries to %s" % (len(outdata), fixturefile))
    
if __name__ == "__main__":
    myndigheter = []
    if len(sys.argv) != 3:
        print("Usage: %s [yamlfile] [fixture]" % sys.argv[0])
        sys.exit()
    yamlfile = sys.argv[1]
    fixture = sys.argv[2]
    make_groups_and_users(yamlfile, fixture)
