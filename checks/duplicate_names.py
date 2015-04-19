
def check_all(members_raw):
    members_by_name = {}
    duplicates = []
    for member_raw in members_raw:
        if member_raw['Kurzname'] in members_by_name:
            duplicates.append(member_raw['Kurzname'])
        else:
            members_by_name[member_raw['Kurzname']] = member_raw

    return (len(duplicates) == 0, duplicates)

import unittest
class Testcases(unittest.TestCase):
    def test_success_empty_list(self):
        self.assertEqual(check_all([]), (True, []))

    def test_success_no_duplicates(self):
        self.assertEqual(check_all([{'Kurzname':'foo'},{'Kurzname':'bar'}]), (True, []))

    def test_fail_duplicates(self):
        self.assertEqual(check_all([{'Kurzname':'foo'},{'Kurzname':'foo'}]), (False, ['foo']))

    def test_exception_none(self):
        with self.assertRaises(TypeError):
            check_all(None)
