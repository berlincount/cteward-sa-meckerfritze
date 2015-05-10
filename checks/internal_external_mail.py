def check_member(member_raw):
    if member_raw['Telefon3'] and member_raw['Telefon3'].endswith('@c-base.org'):
        return (False, "external mailaddress points to internal mailaddress '%s'" % member_raw['Telefon3'])
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'Telefon3': 'user@example.com',
        }),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'Telefon3': 'user@c-base.org'
        }),(False, "external mailaddress points to internal mailaddress 'user@c-base.org'"))
