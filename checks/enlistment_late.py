import dateutil.parser
import datetime
import pytz

def check_member(member_raw):
    if member_raw['Eintritt'] and dateutil.parser.parse(member_raw['Eintritt']) > datetime.datetime.now(pytz.timezone('Europe/Berlin'))+datetime.timedelta(weeks=56):
        return (False, 'member enlistment starts in more than a year')
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'Eintritt': '2015-01-01T00:00:00.000Z',
        }),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'Eintritt': '3015-01-01T00:00:00.000Z',
        }),(False, 'member enlistment starts in more than a year'))
