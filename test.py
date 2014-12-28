#!/usr/bin/env python

import os
import requests
import traceback

# ensure utf-8 encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/cacert.org.pem'

warnings          = {}
members_by_name   = {}
members_by_number = {}

def main():
    try:
        # using ~/.netrc for authentication
        r = requests.get('https://vorstand.c-base.org/cteward-api/legacy/member/*/raw')

        if r.status_code != 200:
            print "Server request failed, code %d\n" % r.status_code
            print r.text
            sys.exit(1)
        for member in r.json():
            if member['Kurzname'] in members_by_name:
                if 'duplicate_names' in warnings:
                    warnings['duplicate_names'] += 1
                else:
                    warnings['duplicate_names']  = 1
                print "DETAIL: duplicate_names: %s" % member['Kurzname']
            else:
                members_by_name[member['Kurzname']] = member

            if member['AdrNr'] in members_by_number:
                if 'duplicate_numbers' in warnings:
                    warnings['duplicate_numbers'] += 1
                else:
                    warnings['duplicate_numbers']  = 1
                print "DETAIL: duplicate_numbers: %s" % member['AdrNr']
            else:
                members_by_number[member['AdrNr']] = member

        for member in members_by_number:
            if members_by_number[member]['MITGLNR'] == None or int(members_by_number[member]['AdrNr']) != int(members_by_number[member]['MITGLNR']):
                if 'number_mismatch' in warnings:
                    warnings['number_mismatch'] += 1
                else:
                    warnings['number_mismatch']  = 1
                mitglnr_int = 0 if members_by_number[member]['MITGLNR'] == None else int(members_by_number[member]['MITGLNR'])
                print "DETAIL: number_mismatch: %s != %s" % (members_by_number[member]['AdrNr'], mitglnr_int)

            if members_by_number[member]['MITGLNR'] == None or "%04d" % int(members_by_number[member]['MITGLNR']) != members_by_number[member]['MITGLNR']:
                if 'number_misformatted' in warnings:
                    warnings['number_misformatted'] += 1
                else:
                    warnings['number_misformatted']  = 1
                mitglnr_formatted = 'None' if members_by_number[member]['MITGLNR'] == None else "%04d" % int(members_by_number[member]['MITGLNR'])
                print "DETAIL: number_misformatted: %s != %s" % (mitglnr_formatted, members_by_number[member]['MITGLNR'])

        if len(warnings) > 0:
            print "Warnings where given:\n"
            for warning in warnings:
                print "%s: %d" % (warning, warnings[warning])

    except KeyboardInterrupt:
        print "Shutdown requested...exiting"
    except requests.exceptions.SSLError as e:
        print "SSL certificate error.\n"
        print e
        sys.exit(1)
    except Exception as e:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

if __name__ == "__main__":
    main()
