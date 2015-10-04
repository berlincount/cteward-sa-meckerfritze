#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import inspect
import requests
import traceback
from prettytable import PrettyTable
from datetime import date

# ensure utf-8 encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def pingler():
    # ensure CAcert bundle is available
    if 'REQUESTS_CA_BUNDLE' not in os.environ:
        os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/cacert.org.pem'

    # getting all of the member information
    try:
        # using ~/.netrc for authentication
        r = requests.get('https://vorstand.c-base.org/cteward-api/legacy/member/*')

        if r.status_code != 200:
            print "Server request failed, code %d\n" % r.status_code
            print r.text
            sys.exit(1)
        members_arr = r.json()['results']

    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except requests.exceptions.SSLError as e:
        print "SSL certificate error.\n"
        print e
        sys.exit(1)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1);

    members = {}
    for member in sorted(members_arr):
        # FIXME: we're assuming this is always set & unique (it should be)
        members[member['Crewname']] = member

    # getting all of the member information
    try:
        # using ~/.netrc for authentication
        r = requests.get('https://vorstand.c-base.org/cteward-api/legacy/member/*/raw')

        if r.status_code != 200:
            print "Server request failed, code %d\n" % r.status_code
            print r.text
            sys.exit(1)
        members_raw_arr = r.json()

    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except requests.exceptions.SSLError as e:
        print "SSL certificate error.\n"
        print e
        sys.exit(1)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
        sys.exit(1);

    members_raw = {}
    for member_raw in sorted(members_raw_arr):
        # FIXME: we're assuming this is always set & unique (it should be)
        members_raw[member_raw['Kurzname']] = member_raw

    contributions = {}
    for member in sorted(members):
        # getting all of the contribution information
        try:
            # using ~/.netrc for authentication
            r = requests.get('https://vorstand.c-base.org/cteward-api/legacy/member/%s/contributions' % member)

            if r.status_code != 200:
                print "Server request failed, code %d\n" % r.status_code
                print r.text
                sys.exit(1)
            contributions[member] = r.json()
        except KeyboardInterrupt:
            print "Shutdown requested...exiting"
        except requests.exceptions.SSLError as e:
            print "SSL certificate error.\n"
            print e
            sys.exit(1)
        except Exception as e:
            traceback.print_exc(file=sys.stdout)
            sys.exit(1);

    if len(contributions) > 0:
        x = PrettyTable([
            "Crewname",
            "Status",
            "T",
            "Err",
            "Vorher",
            str(date.today().year-3),
            str(date.today().year-2),
            str(date.today().year-1),
            str(date.today().year),
            "Gesamt",
            "M",
            "Kontakt",
            "N"
        ])
        x.align["Crewname"]               = "l"
        x.align["Status"]                 = "l"
        x.align["T"]                      = "l"
        x.align["Err"]                    = "r"
        x.align["Vorher"]                 = "r"
        x.align[str(date.today().year-3)] = "r"
        x.align[str(date.today().year-2)] = "r"
        x.align[str(date.today().year-1)] = "r"
        x.align[str(date.today().year)  ] = "r"
        x.align["Gesamt"]                 = "r"
        x.align["M"]                      = "r"
        x.align["Kontakt"]                = "r"
        x.align["N"]                      = "r"

        maxlen_name = 0
        maxlen_stat = 0
        error_total = 0
        yearb_total = 0 # Years before
        yearx_total = 0 # Year-3
        yeary_total = 0 # Year-2
        yearz_total = 0 # Year-1
        yearn_total = 0 # Year (now)
        total_total = 0
        for contributor in sorted(contributions):
            if contributions[contributor]['total']['unpaid'] == 0:
                continue

            if len(contributor) > maxlen_name:
                maxlen_name = len(contributor)

            if len(members[contributor]['Status']) > maxlen_stat:
                maxlen_stat = len(members[contributor]['Status'])

            yearb_sum = 0 # Sum for years before
            yearb = ""    # Years before
            yearx = ""    # Year-3
            yeary = ""    # Year-2
            yearz = ""    # Year-1
            yearn = ""    # Year (now)
            for year in contributions[contributor]['years']:
                if year == str(date.today().year):
                    yearn = u"%.02f€" % contributions[contributor]['years'][year]['unpaid']
                    yearn_total += contributions[contributor]['years'][year]['unpaid']
                elif year == str(date.today().year-1):
                    yearz = u"%.02f€" % contributions[contributor]['years'][year]['unpaid']
                    yearz_total += contributions[contributor]['years'][year]['unpaid']
                elif year == str(date.today().year-2):
                    yeary = u"%.02f€" % contributions[contributor]['years'][year]['unpaid']
                    yeary_total += contributions[contributor]['years'][year]['unpaid']
                elif year == str(date.today().year-3):
                    yearx = u"%.02f€" % contributions[contributor]['years'][year]['unpaid']
                    yearx_total += contributions[contributor]['years'][year]['unpaid']
                else:
                    yearb_sum   += contributions[contributor]['years'][year]['unpaid']
                    yearb = u"%.02f€" % yearb_sum
                    yearb_total += contributions[contributor]['years'][year]['unpaid']
            x.add_row([
                contributor,
                members[contributor]['Status'],
                members_raw[contributor]['Zahlungsart'],
                "???",
                yearb,
                yearx,
                yeary,
                yearz,
                yearn,
                u"%.02f€" % contributions[contributor]['total']['unpaid'],
                "?",
                "--.--.----",
                "?"
            ])
            total_total += contributions[contributor]['total']['unpaid']

        x.add_row([
            '=' * maxlen_name,
            '=' * maxlen_stat,
            "=",
            "===",
            "=" * len(u"%.02f€" % yearb_total),
            "=" * len(u"%.02f€" % yearx_total),
            "=" * len(u"%.02f€" % yeary_total),
            "=" * len(u"%.02f€" % yearz_total),
            "=" * len(u"%.02f€" % yearn_total),
            "=" * len(u"%.02f€" % total_total),
            "=",
            "==========",
            "="
        ])
        x.add_row([
            "",
            "Total",
            "",
            "???",
            u"%.02f€" % yearb_total,
            u"%.02f€" % yearx_total,
            u"%.02f€" % yeary_total,
            u"%.02f€" % yearz_total,
            u"%.02f€" % yearn_total,
            u"%.02f€" % total_total,
            "",
            "",
            ""
        ])
        print x

        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    pingler()
