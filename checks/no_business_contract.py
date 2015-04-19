# -*- coding: utf-8 -*-

# 7;Firmenmitglied;m;2011;1;170

def check_member(member_raw, contracts_raw):
    if member_raw['Betreung'] == 'WEIBLICH' or member_raw['Betreung'] == 'MÄNNLICH':
        return (True,)
    if len (contracts_raw) and all(int(contract_raw['Art']) == 7 and contract_raw['ArtName'] == 'Firmenmitglied' for contract_raw in contracts_raw):
        return (True,)
    return (False, 'no business contract');

# TODO: check whether the contract is active at all?!?

import unittest
class Testcases(unittest.TestCase):
    def test_success_female(self):
        self.assertEqual(check_member({
            'Betreung': 'WEIBLICH',
        },None),(True,))

    def test_success_female(self):
        self.assertEqual(check_member({
            'Betreung': 'MÄNNLICH',
        },None),(True,))

    def test_success_business_contract(self):
        self.assertEqual(check_member({
            'Betreung': '',
        },[{
            'Art': 7,
            'ArtName': 'Firmenmitglied'
        }]),(True,))

    def test_fail_no_contracts(self):
        self.assertEqual(check_member({
            'Betreung': '',
        },[]),(False, 'no business contract'))

    def test_fail_other_contract(self):
        self.assertEqual(check_member({
            'Betreung': '',
        },[{
            'Art': 1,
            'ArtName': 'Member (Regulär)'
        }]),(False, 'no business contract'))
