#!/usr/bin/env python

import pkgutil
import sys
import inspect
import os
import requests
import traceback
from prettytable import PrettyTable
from pprint import pprint

# ensure utf-8 encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

baseurl = 'http://0.0.0.0:14333'

# ensure CAcert bundle is available
if 'REQUESTS_CA_BUNDLE' not in os.environ:
    os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/cacert.org.pem'

# load all checker modules
import checks
def load_all_modules_from_dir(dirname):
    for importer, package_name, _ in pkgutil.iter_modules([dirname]):
        full_package_name = '%s.%s' % (dirname, package_name)
        if full_package_name not in sys.modules:
            module = importer.find_module(package_name
                        ).load_module(full_package_name)

load_all_modules_from_dir('checks')

# getting all of the member information
members = {}
try:
    # using ~/.netrc for authentication
    r = requests.get('%s/legacy/member/*' % baseurl)

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
    r = requests.get('%s/legacy/member/*/raw' % baseurl)

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

# caches for additional data
member_contracts_raw = {}

# call all checker modules
warnings        = {}
acknowledged    = {}
ignored         = {}
verbose         = True
verbose_ignored = True
verbose_trailer = "meckerfritze verbose details:\n"

check_all = sorted([mod for mod in sys.modules.copy() if hasattr(sys.modules[mod], 'check') and mod.startswith('checks.a')])
for mod in check_all:
    check_func = getattr(sys.modules[mod], 'check')
    check_id    = mod.split('.',1)[1]
    check_name  = check_id.split('_',1)[1]
    check_flags = list(check_id.split('_',1)[0])
    if mod.startswith('checks.a_'):
        result = check_func(members,check_name)
    elif mod.startswith('checks.ar_'):
        result = check_func(members_raw,check_name)
    else:
        raise Exception("Unknown check type for check_all")

    if result[0] == False:
        warnings[check_name]      = len(result[1])
        acknowledged[check_name]  = 0
        ignored[check_name]       = 0
        if verbose:
            if verbose_trailer:
                print verbose_trailer
                verbose_trailer = False
            print check_name
            for warn in result[1]:
                print " ", warn

if not verbose_trailer:
    print

check_member = sorted([mod for mod in sys.modules.copy() if hasattr(sys.modules[mod], 'check') and mod.startswith('checks.') and not mod.startswith('checks.a')])

for member_raw in sorted(members_raw):
    # FIXME: we're assuming this always resolves (it should)
    member = [member for member in members if int(member["Adressnummer"]) == int(member_raw['AdrNr'])][0]
    #if not int(member["Adressnummer"]) in [223, 711, 737]:
    #    continue

    verbose_member_header = True
    for mod in check_member:
        check_func  = getattr(sys.modules[mod], 'check')
        check_id    = mod.split('.',1)[1]
        check_name  = check_id.split('_',1)[1]
        check_flags = list(check_id.split('_',1)[0])

        # get additional data
        contracts   = None
        if 'c' in check_flags:
            if not member["Adressnummer"] in member_contracts_raw:
                try:
                    # using ~/.netrc for authentication
                    r = requests.get('%s/legacy/member/%s/contract/*/raw' % (baseurl,member['Crewname']))

                    if r.status_code != 200:
                        print "Server request failed, code %d\n" % r.status_code
                        print r.text
                        sys.exit(1)
                    member_contracts_raw[member["Adressnummer"]] = r.json()
                except KeyboardInterrupt:
                    print "Shutdown requested...exiting"
                except requests.exceptions.SSLError as e:
                    print "SSL certificate error.\n"
                    print e
                    sys.exit(1)
                except Exception as e:
                    traceback.print_exc(file=sys.stdout)
                    sys.exit(1);

            contracts = member_contracts_raw[member["Adressnummer"]]

        # call all checker modules
        debits      = None
        withdrawals = None
        if 'r' not in check_flags:
            result = check_func(member,contracts=contracts,debits=debits,name=check_name)
        elif 'r' in check_flags:
            result = check_func(member_raw,contracts=contracts,debits=debits,name=check_name)
        else:
            raise Exception("Unknown check type")

        if result[0] == False:
            warn = 0
            ack  = 0
            ign  = 0

            if member["Status"] in ['blocked', 'ex-crew', 'ex-raumfahrer']:
                ign  = 1
            else:
                warn = 1

            if check_name in warnings:
                warnings[check_name]     += warn
                acknowledged[check_name] += ack
                ignored[check_name]      += ign
            else:
                warnings[check_name]      = warn
                acknowledged[check_name]  = ack
                ignored[check_name]       = ign

            if verbose and (warn or verbose_ignored):
                if verbose_trailer:
                    print verbose_trailer
                    verbose_trailer = False
                if verbose_member_header:
                    print "member (%d/'%s'):" % (int(member['Adressnummer']), member['Crewname'])
                    verbose_member_header = False
                print " %s: %s" % (check_name, result[1])

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
