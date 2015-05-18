import dateutil.parser
from dateutil.tz import tzutc
import datetime
import itertools

from pprint import pprint

def overlapdays(contract_a, contract_b):
  now = datetime.datetime.now(tzutc())
  if not contract_a['VertragBegin']:
    return float('NaN')
  else:
    contract_a_start = dateutil.parser.parse(contract_a['VertragBegin'])
  if not contract_a['VertragEnde']:
    if contract_a_start > now:
      contract_a_end = contract_a_start
    else:
      contract_a_end = now
  else:
    contract_a_end = dateutil.parser.parse(contract_a['VertragEnde'])

  if not contract_b['VertragBegin']:
    return float('NaN')
  else:
    contract_b_start = dateutil.parser.parse(contract_b['VertragBegin'])
  if not contract_b['VertragEnde']:
    if contract_b_start > now:
      contract_b_end = contract_b_start
    else:
      contract_b_end = now
  else:
    contract_b_end = dateutil.parser.parse(contract_b['VertragEnde'])

  latest_start = max(contract_a_start, contract_b_start)
  earliest_end = min(contract_a_end,   contract_b_end)

  # negative numbers mean gaps
  return (earliest_end - latest_start).days+1

def check_member(member_raw, contracts_raw):
    if not member_raw['Eintritt'] or len(contracts_raw) <= 1:
        return (True,)

    message = ''
    for a,b in itertools.combinations(contracts_raw,2):
        result = overlapdays(a,b)
        if (result > 0):
            if message != '':
                message += ', '
            message += "contracts %d & %d overlap by %d days" % (int(a['VertragNr']),int(b['VertragNr']),result)

    if message != '':
        return (False, message)
    else:
        return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_overlap_error(self):
        self.assertNotEqual(overlapdays({
            'VertragBegin': False,
            'VertragEnde':  False,
            },{
            'VertragBegin': False,
            'VertragEnde':  False,
            }), 0)

    def test_overlap_none(self):
        self.assertEqual(overlapdays({
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
            }), 0)

    def test_overlap_none_open(self):
        self.assertEqual(overlapdays({
            'VertragBegin': '2014-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-09-30T00:00:00.000Z'
            },{
            'VertragBegin': '2015-10-01T00:00:00.000Z',
            'VertragEnde':  None,
            }), 0)

    def test_overlap_one_end(self):
        self.assertEqual(overlapdays({
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-01T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
            }), 1)

    def test_overlap_one_gap(self):
        self.assertEqual(overlapdays({
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-29T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
            }), -1)

    def test_overlap_one_middle(self):
        self.assertEqual(overlapdays({
            'VertragBegin': '2015-05-23T00:00:00.000Z',
            'VertragEnde':  '2015-05-23T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
            }), 1)

    def test_overlap_one_month(self):
        self.assertEqual(overlapdays({
            'VertragBegin': '2015-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-08-31T00:00:00.000Z'
            }), 31)

    def test_overlap_one_month_gap(self):
        self.assertEqual(overlapdays({
            'VertragBegin': '2015-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-03-31T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-08-31T00:00:00.000Z'
            }), -30)

    def test_success_no_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{}]),(True,))

    def test_success_single_contract(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragBegin': '2015-01-01T00:00:00.000Z'
        }]),(True,))

    def test_success_multiple_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
        }]),(True,))

    def test_success_multiple_contracts_open(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragBegin': '2014-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-09-30T00:00:00.000Z'
            },{
            'VertragBegin': '2015-10-01T00:00:00.000Z',
            'VertragEnde':  None
        }]),(True,))

    def test_success_multiple_contracts_gap(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragBegin': '2015-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-03-30T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
        }]),(True,))

    def test_fail_multiple_contracts_single(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr':    1,
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragNr':    2,
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragNr':    3,
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
        }]),(False, "contracts 1 & 2 overlap by 30 days"))

    def test_fail_multiple_contracts_multiple(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr':    1,
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragNr':    2,
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragNr':    3,
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
            },{
            'VertragNr':    4,
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
        }]),(False, "contracts 1 & 2 overlap by 30 days, contracts 3 & 4 overlap by 31 days"))
