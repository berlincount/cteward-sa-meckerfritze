#!/usr/bin/env python

import pkgutil
import sys
import inspect
import os
import requests
import traceback
from prettytable import PrettyTable

# ensure utf-8 encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# ensure CAcert bundle is available
if 'REQUESTS_CA_BUNDLE' not in os.environ:
    os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/cacert.org.pem'

# load all checker modules
def load_all_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        if full_package_name not in sys.modules:
            module = importer.find_module(package_name
                        ).load_module(full_package_name)

load_all_modules_from_dir('checks_members')
load_all_modules_from_dir('checks_members_raw')
load_all_modules_from_dir('checks_member')
load_all_modules_from_dir('checks_member_raw')

# getting all of the member information
members = {}
try:
    # using ~/.netrc for authentication
    r = requests.get('https://vorstand.c-base.org/cteward-api/legacy/member/*')

    if r.status_code != 200:
        print "Server request failed, code %d\n" % r.status_code
        print r.text
        sys.exit(1)
    members = r.json()['results']

except KeyboardInterrupt:
    print "Shutdown requested...exiting"
except requests.exceptions.SSLError as e:
    print "SSL certificate error.\n"
    print e
    sys.exit(1)
except Exception as e:
    traceback.print_exc(file=sys.stdout)
    sys.exit(1);

# getting all of the member information (raw)
members_raw = {}
try:
    # using ~/.netrc for authentication
    r = requests.get('https://vorstand.c-base.org/cteward-api/legacy/member/*/raw')

    if r.status_code != 200:
        print "Server request failed, code %d\n" % r.status_code
        print r.text
        sys.exit(1)
    members_raw = r.json()

except KeyboardInterrupt:
    print "Shutdown requested...exiting"
except requests.exceptions.SSLError as e:
    print "SSL certificate error.\n"
    print e
    sys.exit(1)
except Exception as e:
    traceback.print_exc(file=sys.stdout)
    sys.exit(1);

# call all checker modules
warnings     = {}
acknowledged = {}
ignored      = {}
verbose = True
verbose_trailer = "meckerfritze verbose details:\n"

check_members     = sorted([mod for mod in sys.modules if mod.startswith('checks_members.')])
for mod in check_members:
    check_func = getattr(sys.modules[mod], 'check')
    result = check_func(members,mod.split('.',2)[1])
    if result[0] == False:
        warnings[mod]      = len(result[1])
        acknowledged[mod]  = 0
        ignored[mod]       = 0
        if verbose:
            if verbose_trailer:
                print verbose_trailer
                verbose_trailer = False
            print mod
            for warn in result[1]:
                print " ", warn


check_members_raw = sorted([mod for mod in sys.modules if mod.startswith('checks_members_raw.')])
for mod in check_members_raw:
    check_func = getattr(sys.modules[mod], 'check')
    result = check_func(members_raw,mod.split('.',2)[1])
    if result[0] == False:
        warnings[mod]      = len(result[1])
        acknowledged[mod]  = 0
        ignored[mod]       = 0
        if verbose:
            if verbose_trailer:
                print verbose_trailer
                verbose_trailer = False
            print mod
            for warn in result[1]:
                print " ", warn

if not verbose_trailer:
    print

check_member      = sorted([mod for mod in sys.modules if mod.startswith('checks_member.')])
check_member_raw  = sorted([mod for mod in sys.modules if mod.startswith('checks_member_raw.')])

for member_raw in sorted(members_raw):
    # FIXME: we're assuming this always resolves (it should)
    member = [member for member in members if int(member["Adressnummer"]) == int(member_raw['AdrNr'])][0]

    verbose_member_header = True
    for mod in check_member:
        check_func = getattr(sys.modules[mod], 'check')
        result = check_func(member, mod.split('.',2)[1])
        if result[0] == False:
            if mod in warnings:
                warnings[mod]     += 1
                acknowledged[mod]  = 0
                ignored[mod]       = 0
            else:
                warnings[mod]      = 1
                acknowledged[mod]  = 0
                ignored[mod]       = 0

            if verbose:
                if verbose_trailer:
                    print verbose_trailer
                    verbose_trailer = False
                if verbose_member_header:
                    print "member (%d/'%s'):" % (int(member['Adressnummer']), member['Crewname'])
                    verbose_member_header = False
                print " ", mod, result[1]

    for mod in check_member_raw:
        check_func = getattr(sys.modules[mod], 'check')
        result = check_func(member_raw, mod.split('.',2)[1])
        if result[0] == False:
            if mod in warnings:
                warnings[mod]     += 1
                acknowledged[mod]  = 0
                ignored[mod]       = 0
            else:
                warnings[mod]      = 1
                acknowledged[mod]  = 0
                ignored[mod]       = 0

            if verbose:
                if verbose_trailer:
                    print verbose_trailer
                    verbose_trailer = False
                if verbose_member_header:
                    print "member (%d/'%s'):" % (int(member_raw['AdrNr']), member_raw['Kurzname'])
                    verbose_member_header = False
                print " ", mod, result[1]

    if not verbose_member_header:
        print

if len(warnings) > 0:
    if verbose:
        print

    print "meckerfritze warning statistics:\n"

    x = PrettyTable(["Name","warn","ack","ign"])
    x.align["Name"] = "l"
    x.align["warn"] = "r"
    x.align["ack"]  = "r"
    x.align["ign"]  = "r"
    for warning in sorted(warnings):
        x.add_row([warning, warnings[warning], acknowledged[warning], ignored[warning]])
    print x

    sys.exit(1)
else:
    sys.exit(0)
