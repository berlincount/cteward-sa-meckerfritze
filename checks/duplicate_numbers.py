
def check_all(members_raw):
    members_by_number = {}
    duplicates = []
    for member_raw in members_raw:
        if member_raw['AdrNr'] in members_by_number:
            duplicates.append(member_raw['AdrNr'])
        else:
            members_by_number[member_raw['AdrNr']] = member_raw

    return (len(duplicates) == 0, duplicates)

import unittest
class Testcases(unittest.TestCase):
    def test_success_empty_list(self):
        self.assertEqual(check_all([]), (True, []))

    def test_success_no_duplicates(self):
        self.assertEqual(check_all([{'AdrNr':'123'},{'AdrNr':'456'}]), (True, []))

    def test_fail_duplicates(self):
        self.assertEqual(check_all([{'AdrNr':'123'},{'AdrNr':'123'}]), (False, ['123']))

    def test_exception_none(self):
        with self.assertRaises(TypeError):
            check_all(None)
