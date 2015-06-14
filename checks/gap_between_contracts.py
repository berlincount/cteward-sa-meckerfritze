from dateutil.tz import tzutc
import itertools

# reuse code
from overlapping_contracts import overlapdays

def check_member(member_raw, contracts_raw):
    if not member_raw['Eintritt'] or len(contracts_raw) <= 1:
        return (True,)

    message = ''
    for a,b in itertools.combinations(contracts_raw,2):
        # skip non-neighbouring contracts
        if int(b['VertragNr'] and b['VertragNr'] or 0)-int(a['VertragNr'] and a['VertragNr'] or 0) != 1:
            continue

        result = overlapdays(a,b)
        if (result < 0):
            if message != '':
                message += ', '
            message += "contracts %d & %d have a gap of %d days" % (int(a['VertragNr'] and a['VertragNr'] or 0),int(b['VertragNr'] and b['VertragNr'] or 0),-result)

    if message != '':
        return (False, message)
    else:
        return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success_no_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[]),(True,))

    def test_success_single_contract(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragBegin': '2015-01-01T00:00:00.000Z'
        }]),(True,))

    def test_success_two_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr':    '1',
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragNr':    '2',
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
        }]),(True,))

    def test_success_two_contracts_open(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr':    '1',
            'VertragBegin': '2014-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-09-30T00:00:00.000Z'
            },{
            'VertragNr':    '2',
            'VertragBegin': '2015-10-01T00:00:00.000Z',
            'VertragEnde':  None
        }]),(True,))

    def test_success_three_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr':    '1',
            'VertragBegin': '2015-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-01-31T00:00:00.000Z'
            },{
            'VertragNr':    '2',
            'VertragBegin': '2015-02-01T00:00:00.000Z',
            'VertragEnde':  '2015-02-28T00:00:00.000Z'
            },{
            'VertragNr':    '3',
            'VertragBegin': '2015-03-01T00:00:00.000Z',
            'VertragEnde':  '2015-03-31T00:00:00.000Z'
        }]),(True,))

    def test_fail_multiple_contracts_gap(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr':    '1',
            'VertragBegin': '2015-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-03-30T00:00:00.000Z'
            },{
            'VertragNr':    '2',
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
        }]),(False, "contracts 1 & 2 have a gap of 31 days"))
