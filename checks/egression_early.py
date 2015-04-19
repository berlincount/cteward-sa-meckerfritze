import dateutil.parser

def check_member(member_raw):
    if member_raw['Austritt'] and dateutil.parser.parse(member_raw['Austritt']) < dateutil.parser.parse('1995-08-12T00:00:00.000Z'):
        return (False, "member discharged before c-base was founded")
    return (True,)
