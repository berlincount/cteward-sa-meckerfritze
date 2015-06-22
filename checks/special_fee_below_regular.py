# -*- coding: utf-8 -*-
# 5;Member (Sonder);m;2008;1;0

def check_member(member_raw, contracts_raw):
    if len (contracts_raw) == 0 or all(int(contract_raw['Art']) != 5 and contract_raw['ArtName'] != 'Member (Sonder)' for contract_raw in contracts_raw):
        return (True,)
    message = "special fee too low:"
    content = ""
    for contract_raw in contracts_raw:
        if contract_raw['Art'] != 5 and contract_raw['ArtName'] != 'Member (Sonder)':
            continue
        if contract_raw['Betrag'] >= 17:
            continue
        content += ' %d:%.2f' % (int(contract_raw['VertragNr']),contract_raw['Betrag'])
    if content == "":
        return (True,)
    return (False, message+content);

# TODO: check whether the contract is active at all?!?

import unittest
class Testcases(unittest.TestCase):
    def test_success_no_contracts(self):
        self.assertEqual(check_member({},[]),(True,))

    def test_success_other_contract(self):
        self.assertEqual(check_member({},[{
            'Art': 1,
            'ArtName': 'Member (Regulär)'
        }]),(True,))

    def test_success_higher_than_regular(self):
        self.assertEqual(check_member({},[{
            'Art': 5,
            'ArtName': 'Member (Sonder)',
            'Betrag': 23.00
        }]),(True,))

    def test_success_exactly_regular(self):
        self.assertEqual(check_member({},[{
            'Art': 5,
            'ArtName': 'Member (Sonder)',
            'Betrag': 17.00
        }]),(True,))

    def test_fail_lower_than_regular(self):
        self.assertEqual(check_member({},[{
            'VertragNr': 1,
            'Art': 5,
            'ArtName': 'Member (Sonder)',
            'Betrag': 15.00
        }]),(False, 'special fee too low: 1:15.00'))
