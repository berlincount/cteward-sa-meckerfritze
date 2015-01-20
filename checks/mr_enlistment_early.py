import dateutil.parser

def check(member_raw, contracts=None, debits=None, withdrawals=None, name='enlistment_early'):
    if member_raw['Eintritt'] and dateutil.parser.parse(member_raw['Eintritt']) < dateutil.parser.parse('1995-08-12T00:00:00.000Z'):
        return (False, "member enlisted before c-base was founded")
    return (True,)
