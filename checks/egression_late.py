import dateutil.parser
from dateutil.tz import tzutc
import datetime

def check_member(member_raw):
    if member_raw['Austritt'] and dateutil.parser.parse(member_raw['Austritt']) > datetime.datetime.now(tzutc())+datetime.timedelta(weeks=56):
        return (False, 'member discharged more than a year in the future')
    return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success(self):
        self.assertEqual(check_member({
            'Austritt': '2015-01-31T00:00:00.000Z',
        }),(True,))

    def test_fail(self):
        self.assertEqual(check_member({
            'Austritt': '3015-01-31T00:00:00.000Z',
        }),(False, 'member discharged more than a year in the future'))
