import dateutil.parser
import datetime

def check_member(member_raw, contracts_raw):
    if member_raw['Eintritt'] and len(contracts_raw) and contracts_raw[0]['VertragBegin'] and dateutil.parser.parse(member_raw['Eintritt'])+datetime.timedelta(days=21) < dateutil.parser.parse(contracts_raw[0]['VertragBegin']):
        return (False, 'first contract of member starts more than 21 days after enlistment')
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'Eintritt': '2015-01-01T00:00:00.000Z',
        },[{
            'VertragBegin': '2015-01-01T00:00:00.000Z',
        }]),(True,))

    def test_success_no_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': '2015-01-01T00:00:00.000Z',
        },[]),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'Eintritt': '2015-01-01T00:00:00.000Z',
        },[{
            'VertragBegin': '2015-02-01T00:00:00.000Z',
        }]),(False,'first contract of member starts more than 21 days after enlistment'))
