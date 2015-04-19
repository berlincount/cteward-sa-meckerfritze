def check_member(member_raw, contracts_raw):
    if contracts_raw == None or len(contracts_raw) == 0:
        return (False, 'no contract');
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({},[{}]),(True,))

    def test_fail_contracts_none(self):
        self.assertEqual(check_member({},None),(False, 'no contract'))

    def test_fail_no_contracts(self):
        self.assertEqual(check_member({},[]),(False, 'no contract'))
