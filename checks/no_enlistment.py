
def check_member(member_raw):
    if not member_raw['Eintritt']:
        return (False, 'member enlistment never started')
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'Eintritt': '2015-01-01T00:00:00.000Z',
        }),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'Eintritt': None,
        }),(False, 'member enlistment never started'))
