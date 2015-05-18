import re

def check_member(member_raw, contracts_raw):
    if not member_raw['Eintritt'] or len(contracts_raw) == 0:
        return (True,)

    numpat = re.compile(r'^[1-9][0-9]{0,2}$')
    message = ""
    count = 1
    for contract in contracts_raw:
        if not numpat.match(contract['VertragNr']):
            if message != '':
                message += ', '
            message += "contract %d in list has bogus nr '%s'" % (count,contract['VertragNr'])
        count += 1

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
            'VertragNr'   : '1',
            'VertragBegin': '2015-01-01T00:00:00.000Z'
        }]),(True,))

    def test_fail_single_contract_empty(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr'   : '',
            'VertragBegin': '2015-01-01T00:00:00.000Z'
        }]),(False, "contract 1 in list has bogus nr ''"))

    def test_fail_single_contract_blank(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr'   : ' ',
            'VertragBegin': '2015-01-01T00:00:00.000Z'
        }]),(False, "contract 1 in list has bogus nr ' '"))

    def test_fail_single_contract_blank_prefix(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr'   : ' 1',
            'VertragBegin': '2015-01-01T00:00:00.000Z'
        }]),(False, "contract 1 in list has bogus nr ' 1'"))

    def test_fail_multple_contract(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr'   : ' 1',
            'VertragBegin': '2015-01-01T00:00:00.000Z'
         },{
            'VertragNr'   : '',
            'VertragBegin': '2015-01-01T00:00:00.000Z'
        }]),(False,"contract 1 in list has bogus nr ' 1', contract 2 in list has bogus nr ''"))
