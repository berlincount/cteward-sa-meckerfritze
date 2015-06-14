def check_member(member_raw, contracts_raw):
    if not member_raw['Eintritt'] or len(contracts_raw) <= 1:
        return (True,)

    message = ''
    lastend = '1970-01-01T00:00:00.000Z'
    lastnum = 0
    for contract in contracts_raw:
        if contract['VertragBegin'] < lastend:
            if message != '':
                message += ', '
            message += "contracts %d and %d seem out of order" % (lastnum,int(contract['VertragNr'] and contract['VertragNr'] or 0))
        lastend = contract['VertragEnde']
        lastnum = int(contract['VertragNr'] and contract['VertragNr'] or 0)

    if message != '':
        return (False, message)
    else:
        return (True,)

import unittest
class Testcases(unittest.TestCase):
    def test_success_no_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[]),(True,))

    def test_success_single_contract(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragBegin': '2015-01-01T00:00:00.000Z'
        }]),(True,))

    def test_success_two_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr':    '1',
            'VertragBegin': '2015-04-01T00:00:00.000Z',
            'VertragEnde':  '2015-04-30T00:00:00.000Z'
            },{
            'VertragNr':    '2',
            'VertragBegin': '2015-05-01T00:00:00.000Z',
            'VertragEnde':  '2015-05-31T00:00:00.000Z'
        }]),(True,))

    def test_success_three_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr':    '1',
            'VertragBegin': '2015-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-01-31T00:00:00.000Z'
            },{
            'VertragNr':    '2',
            'VertragBegin': '2015-02-01T00:00:00.000Z',
            'VertragEnde':  '2015-02-28T00:00:00.000Z'
            },{
            'VertragNr':    '3',
            'VertragBegin': '2015-03-01T00:00:00.000Z',
            'VertragEnde':  '2015-03-31T00:00:00.000Z'
        }]),(True,))

    def test_fail_multiple_contracts(self):
        self.assertEqual(check_member({
            'Eintritt': 'set-to-something',
        },[{
            'VertragNr':    '1',
            'VertragBegin': '2015-01-01T00:00:00.000Z',
            'VertragEnde':  '2015-01-31T00:00:00.000Z'
            },{
            'VertragNr':    '2',
            'VertragBegin': '2015-03-01T00:00:00.000Z',
            'VertragEnde':  '2015-03-31T00:00:00.000Z'
            },{
            'VertragNr':    '3',
            'VertragBegin': '2015-02-01T00:00:00.000Z',
            'VertragEnde':  '2015-02-28T00:00:00.000Z'
        }]),(False,'contracts 2 and 3 seem out of order'))
