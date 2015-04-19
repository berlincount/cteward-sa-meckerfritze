import dateutil.parser
import datetime

def check_member(member_raw, contracts_raw):
    if member_raw['Austritt'] and len(contracts_raw) and contracts_raw[len(contracts_raw)-1]['VertragEnde'] and dateutil.parser.parse(member_raw['Austritt'])+datetime.timedelta(days=21) < dateutil.parser.parse(contracts_raw[len(contracts_raw)-1]['VertragEnde']):
        return (False, 'last contract of member ends more than 21 days after egression')
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'Austritt': '2015-01-31T00:00:00.000Z',
        },[{
            'VertragEnde': '2015-01-31T00:00:00.000Z',
        }]),(True,))

    def test_success_no_contracts(self):
        self.assertEqual(check_member({
            'Austritt': '2015-01-31T00:00:00.000Z',
        },[]),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'Austritt': '2015-01-31T00:00:00.000Z',
        },[{
            'VertragEnde': '2015-02-23T00:00:00.000Z',
        }]),(False,'last contract of member ends more than 21 days after egression'))
