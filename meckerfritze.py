#!/usr/bin/env python

import pkgutil
import inspect
import os
import requests
import traceback
import json
from prettytable import PrettyTable
from pprint import pprint
import argparse

def meckerfritze(mainargs):
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
    member_contracts_raw   = {}
    member_debits_raw      = {}
    member_withdrawals_raw = {}
    member_memo_raw        = {}

    if mainargs.cache:
        if os.path.isfile('member_contracts_raw.json'):
            member_contracts_raw   = json.load( open( "member_contracts_raw.json",   "rb" ) )
        if os.path.isfile('member_debits_raw.json'):
            member_debits_raw      = json.load( open( "member_debits_raw.json",      "rb" ) )
        if os.path.isfile('member_withdrawals_raw.json'):
            member_withdrawals_raw = json.load( open( "member_withdrawals_raw.json", "rb" ) )
        if os.path.isfile('member_memo_raw.json'):
            member_memo_raw        = json.load( open( "member_memo_raw.json",        "rb" ) )

    # call all checker modules
    warnings        = {}
    acknowledged    = {}
    ignored         = {}
    verbose         = mainargs.verbose
    verbose_ignored = mainargs.ignored
    verbose_trailer = "meckerfritze verbose details:\n"
    debug           = mainargs.debug

    ## catch problems
    #check_broken = sorted([mod for mod in sys.modules.copy() if mod.startswith('checks.') and not (hasattr(sys.modules[mod], 'check_all') or hasattr(sys.modules[mod], 'check_member'))])
    #if len(check_broken):
    #    pprint(check_broken)
    #    raise Exception("Broken check modules?")

    check_all = sorted([mod for mod in sys.modules.copy() if hasattr(sys.modules[mod], 'check_all') and mod.startswith('checks.')])
    for mod in check_all:
        check_func = getattr(sys.modules[mod], 'check_all')
        check_name  = mod.split('.',1)[1]
        if mainargs.only and mod != mainargs.only:
            continue
        if 'members' in inspect.getargspec(check_func)[0]:
            if debug:
              print "DBG: check_all (cooked) from %s" % check_name
            result = check_func(members)
        elif 'members_raw' in inspect.getargspec(check_func)[0]:
            if debug:
              print "DBG: check_all (raw) from %s" % check_name
            result = check_func(members_raw)
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

    check_member = sorted([mod for mod in sys.modules.copy() if hasattr(sys.modules[mod], 'check_member') and mod.startswith('checks.')])

    for member_raw in sorted(members_raw, key=lambda member: int(member['AdrNr'])):
        # FIXME: we're assuming this always resolves (it should)
        member = [member for member in members if int(member["Adressnummer"]) == int(member_raw['AdrNr'])][0]
        #if not int(member["Adressnummer"]) in [223, 711, 737]:
        #    continue

        verbose_member_header = True
        for mod in check_member:
            check_func  = getattr(sys.modules[mod], 'check_member')
            check_name  = mod.split('.',1)[1]

            if mainargs.only and check_name != mainargs.only:
              continue

            args = {}
            if 'member' in inspect.getargspec(check_func)[0]:
              args['member'] = member
            elif 'member_raw' in inspect.getargspec(check_func)[0]:
              args['member_raw'] = member_raw

            # get additional data
            if not '%04d' % member["Adressnummer"] in member_memo_raw:
                try:
                    # using ~/.netrc for authentication
                    r = requests.get('%s/legacy/member/%s/memo' % (baseurl,member['Crewname']))

                    if r.status_code != 200:
                        print "Server request failed, code %d\n" % r.status_code
                        print r.text
                        sys.exit(1)
                    member_memo_raw['%04d' % member["Adressnummer"]] = r.json()
                except KeyboardInterrupt:
                    print "Shutdown requested...exiting"
                except requests.exceptions.SSLError as e:
                    print "SSL certificate error.\n"
                    print e
                    sys.exit(1)
                except Exception as e:
                    traceback.print_exc(file=sys.stdout)
                    sys.exit(1);

            if 'contracts_raw' in inspect.getargspec(check_func)[0]:
                if not '%04d' % member["Adressnummer"] in member_contracts_raw:
                    try:
                        # using ~/.netrc for authentication
                        r = requests.get('%s/legacy/member/%s/contract/*/raw' % (baseurl,member['Crewname']))

                        if r.status_code != 200:
                            print "Server request failed, code %d\n" % r.status_code
                            print r.text
                            sys.exit(1)
                        member_contracts_raw['%04d' % member["Adressnummer"]] = r.json()
                    except KeyboardInterrupt:
                        print "Shutdown requested...exiting"
                    except requests.exceptions.SSLError as e:
                        print "SSL certificate error.\n"
                        print e
                        sys.exit(1)
                    except Exception as e:
                        traceback.print_exc(file=sys.stdout)
                        sys.exit(1);

                args['contracts_raw'] = member_contracts_raw['%04d' % member["Adressnummer"]]

            if 'debits_raw' in inspect.getargspec(check_func)[0]:
                if not '%04d' % member["Adressnummer"] in member_debits_raw:
                    try:
                        # using ~/.netrc for authentication
                        r = requests.get('%s/legacy/member/%s/debit/*/raw' % (baseurl,member['Crewname']))

                        if r.status_code != 200:
                            print "Server request failed, code %d\n" % r.status_code
                            print r.text
                            sys.exit(1)
                        member_debits_raw['%04d' % member["Adressnummer"]] = r.json()
                    except KeyboardInterrupt:
                        print "Shutdown requested...exiting"
                    except requests.exceptions.SSLError as e:
                        print "SSL certificate error.\n"
                        print e
                        sys.exit(1)
                    except Exception as e:
                        traceback.print_exc(file=sys.stdout)
                        sys.exit(1);

                args['debits_raw'] = member_debits_raw['%04d' % member["Adressnummer"]]

            if 'withdrawals_raw' in inspect.getargspec(check_func)[0]:
                if not '%04d' % member["Adressnummer"] in member_withdrawals_raw:
                    try:
                        # using ~/.netrc for authentication
                        r = requests.get('%s/legacy/member/%s/withdrawal/*/raw' % (baseurl,member['Crewname']))

                        if r.status_code != 200:
                            print "Server request failed, code %d\n" % r.status_code
                            print r.text
                            sys.exit(1)
                        member_withdrawals_raw['%04d' % member["Adressnummer"]] = r.json()
                    except KeyboardInterrupt:
                        print "Shutdown requested...exiting"
                    except requests.exceptions.SSLError as e:
                        print "SSL certificate error.\n"
                        print e
                        sys.exit(1)
                    except Exception as e:
                        traceback.print_exc(file=sys.stdout)
                        sys.exit(1);

                args['withdrawals_raw'] = member_withdrawals_raw['%04d' % member["Adressnummer"]]

            # call all checker modules
            if debug:
              print "DBG: check_member (..) from %s" % check_name
              pprint(args.keys())
            result = check_func(**args)

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
                        print "member (%d/'%s')%s:" % (int(member['Adressnummer']), member['Crewname'], ign and ' -- INACTIVE!' or '')
                        verbose_member_header = False
                    print " %s: %s" % (check_name, result[1])

        if not verbose_member_header:
            print

    if mainargs.cache:
            json.dump( member_contracts_raw,   open( "member_contracts_raw.json",   "wb" ), sort_keys=True, indent=4, separators=(',', ': '))
            json.dump( member_debits_raw,      open( "member_debits_raw.json",      "wb" ), sort_keys=True, indent=4, separators=(',', ': '))
            json.dump( member_withdrawals_raw, open( "member_withdrawals_raw.json", "wb" ), sort_keys=True, indent=4, separators=(',', ': '))
            json.dump( member_memo_raw,        open( "member_memo_raw.json",        "wb" ), sort_keys=True, indent=4, separators=(',', ': '))

    totals = {'warnings': 0, 'acknowledged': 0, 'ignored': 0}
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
            totals['warnings']     += warnings[warning]
            totals['acknowledged'] += acknowledged[warning]
            totals['ignored']      += ignored[warning]
        x.add_row(['======================','====','====','===='])
        x.add_row(['Total',totals['warnings'],totals['acknowledged'],totals['ignored']])
        print x

        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cache',        help='use caching (debug only)', action='store_true')
    parser.add_argument('--verbose',      help='show details', action='store_true')
    parser.add_argument('--acknowledged', help='show also acknowledged problems (with verbose only)', action='store_true')
    parser.add_argument('--ignored',      help='show also problems with ex-members (with verbose only)', action='store_true')
    parser.add_argument('--debug',        help='show check calls', action='store_true')
    parser.add_argument('--only',         help='only run a specific check')
    meckerfritze(parser.parse_args())
