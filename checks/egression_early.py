import dateutil.parser

def check_member(member_raw):
    if member_raw['Austritt'] and dateutil.parser.parse(member_raw['Austritt']) < dateutil.parser.parse('1995-08-12T00:00:00.000Z'):
        return (False, 'member discharged before c-base was founded')
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'Austritt': '2015-01-31T00:00:00.000Z',
        }),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'Austritt': '1995-08-11T00:00:00.000Z',
        }),(False,'member discharged before c-base was founded'))
