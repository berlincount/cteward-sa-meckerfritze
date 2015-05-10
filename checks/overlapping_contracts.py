import dateutil.parser
from dateutil.tz import tzutc
import datetime
import itertools

from pprint import pprint

def overlapdays(contract_a, contract_b):
  if not contract_a['VertragBegin']:
    return 99999 # TODO: should raise or something
  else:
    contract_a_start = dateutil.parser.parse(contract_a['VertragBegin'])
  if not contract_a['VertragEnde']:
    contract_a_end = datetime.datetime.now(tzutc())
  else:
    contract_a_end = dateutil.parser.parse(contract_a['VertragEnde'])

  if not contract_b['VertragBegin']:
    return 99999 # TODO: should raise or something
  else:
    contract_b_start = dateutil.parser.parse(contract_b['VertragBegin'])
  if not contract_b['VertragEnde']:
    contract_b_end = datetime.datetime.now(tzutc())
  else:
    contract_b_end = dateutil.parser.parse(contract_b['VertragEnde'])

  latest_start = max(contract_a_start, contract_b_start)
  earliest_end = min(contract_a_end,   contract_b_end)

  # negative numbers mean gaps
  return (earliest_end - latest_start).days+1

def check_member(member_raw, contracts_raw):
    if member_raw['Eintritt'] and len(contracts_raw) > 1 and not all(overlapdays(a,b) <= 0 for a,b in itertools.permutations(contracts_raw,2)):
        return (False, "some of the member's %d contracts overlap" % len(contracts_raw))
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_overlap_none(self):
        self.assertEqual(overlapdays({
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
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

    def test_fail_multiple_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
        }]),(False, "some of the member's 3 contracts overlap"))
