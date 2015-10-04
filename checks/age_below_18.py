import dateutil.parser
from dateutil.tz import tzutc
import datetime

def yearsago(years, from_date=None):
    if from_date is None:
        from_date = datetime.datetime.now(tzutc())
    try:
        return from_date.replace(year=from_date.year - years)
    except:
        # Must be 2/29!
        assert from_date.month == 2 and from_date.day == 29 # can be removed
        return from_date.replace(month=2, day=28,year=from_date.year-years)

def check_member(member_raw):
    if not member_raw['Geburtsdatum']:
        # no age set :(
        return (True,)
    try:
        dateutil.parser.parse(member_raw['Geburtsdatum'])
    except ValueError:
        return (False, "Geburtsdatum doesn't parse correctly")
    if dateutil.parser.parse(member_raw['Geburtsdatum']) <= yearsago(18):
        return (True,)
    return (False, 'age is not above 18')

import unittest
class Testcases(unittest.TestCase):
    def test_success_exactly_18(self):
        self.assertEqual(check_member({
            'Geburtsdatum': yearsago(18).isoformat(),
        }),(True,))

    def test_success_above_18(self):
        self.assertEqual(check_member({
            'Geburtsdatum': yearsago(21).isoformat(),
        }),(True,))

    def test_success_unset(self):
        self.assertEqual(check_member({
            'Geburtsdatum': None,
        }),(True,))

    def test_fail_failparse(self):
        self.assertEqual(check_member({
            'Geburtsdatum': 'garble garble garbage',
        }),(False, "Geburtsdatum doesn't parse correctly"))

    def test_fail_tooyoung(self):
        self.assertEqual(check_member({
            'Geburtsdatum': yearsago(17).isoformat(),
        }),(False, 'age is not above 18'))

    def test_years_zero_fixed(self):
        self.assertEqual(yearsago(0,  dateutil.parser.parse('2016-02-29')).isoformat(), '2016-02-29T00:00:00')

    def test_years_ten_fixed(self):
        self.assertEqual(yearsago(10, dateutil.parser.parse('2016-02-29')).isoformat(), '2006-02-28T00:00:00')

    def test_years_zero_dynamic(self):
        now = datetime.datetime.now(tzutc())
        self.assertEqual(yearsago(0,  now).isoformat(), now.isoformat())

    def test_years_ten_dynamic(self):
        now = datetime.datetime.now(tzutc())
        if now.month == 2 and now.day == 29:
            tenyearsago = now.replace(year=now.year-10, day=28)
        else:
            tenyearsago = now.replace(year=now.year-10)
        self.assertEqual(yearsago(10, now).isoformat(), tenyearsago.isoformat())
