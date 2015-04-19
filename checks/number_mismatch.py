
def check_member(member_raw):
    if member_raw['MITGLNR'] == None or int(member_raw['AdrNr']) != int(member_raw['MITGLNR']):
        mitglnr_int = 0 if member_raw['MITGLNR'] == None else int(member_raw['MITGLNR'])
        return (False, '%s != %s' % (member_raw['AdrNr'], mitglnr_int))
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'AdrNr': '1234',
            'MITGLNR': '1234',
        }),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'AdrNr': '1234',
            'MITGLNR': '5678',
        }),(False, '1234 != 5678'))
