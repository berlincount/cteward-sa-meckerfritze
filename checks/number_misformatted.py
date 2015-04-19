
def check_member(member_raw):
    if member_raw['MITGLNR'] == None or '%04d' % int(member_raw['MITGLNR']) != member_raw['MITGLNR']:
        mitglnr_formatted = 'None' if member_raw['MITGLNR'] == None else '%04d' % int(member_raw['MITGLNR'])
        return (False, '%s != %s' % (mitglnr_formatted, member_raw['MITGLNR']))
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'MITGLNR': '1234',
        }),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'MITGLNR': '1',
        }),(False, '0001 != 1'))
