import dateutil.parser

def check_member(member_raw):
    if member_raw['Eintritt'] and dateutil.parser.parse(member_raw['Eintritt']) < dateutil.parser.parse('1995-08-12T00:00:00.000Z'):
        return (False, 'member enlisted before c-base was founded')
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'Eintritt': '1995-08-12T00:00:00.000Z',
        }),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'Eintritt': '1995-08-11T00:00:00.000Z',
        }),(False, 'member enlisted before c-base was founded'))
