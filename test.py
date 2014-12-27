#!/usr/bin/env python

import os
import requests
import traceback

# ensure utf-8 encoding
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

os.environ['REQUESTS_CA_BUNDLE'] = '/etc/ssl/certs/cacert.org.pem'

def main():
    try:
        # using ~/.netrc for authentication
        r = requests.get('https://vorstand.c-base.org/cteward-api/legacy/member/')
        if r.status_code != 200:
            print "Server request failed, code %d\n" % r.status_code
            print r.text
            sys.exit(1)
        print "could get data of %d members." % len(r.json()['results'])

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
