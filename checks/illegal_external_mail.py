import re

def check_member(member_raw):
    if not member_raw['Telefon3'] or not re.compile('^[^@]+@[^@]+\.[^@]+$').match(member_raw['Telefon3']):
        return (False, "invalid external mailaddress '%s'" % member_raw['Telefon3'])
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'Telefon3': 'user@example.com',
        }),(True,))

    def test_fail_mail_empty(self):
        self.assertEqual(check_member({
            'Telefon3': '',
        }),(False, "invalid external mailaddress ''"))

    def test_fail_mail_bogus(self):
        self.assertEqual(check_member({
            'Telefon3': 'blah blah blah',
        }),(False, "invalid external mailaddress 'blah blah blah'"))

    def test_fail_mail_multiple(self):
        self.assertEqual(check_member({
            'Telefon3': 'user@example.com,user@example.com',
        }),(False, "invalid external mailaddress 'user@example.com,user@example.com'"))
