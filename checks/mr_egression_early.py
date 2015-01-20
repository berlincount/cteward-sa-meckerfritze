import dateutil.parser

def check(member_raw, contracts=None, debits=None, withdrawals=None, name='egression_early'):
    if member_raw['Austritt'] and dateutil.parser.parse(member_raw['Austritt']) < dateutil.parser.parse('1995-08-12T00:00:00.000Z'):
        return (False, "member discharged before c-base was founded")
    return (True,)
