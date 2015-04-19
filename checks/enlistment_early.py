import dateutil.parser

def check_member(member_raw):
    if member_raw['Eintritt'] and dateutil.parser.parse(member_raw['Eintritt']) < dateutil.parser.parse('1995-08-12T00:00:00.000Z'):
        return (False, "member enlisted before c-base was founded")
    return (True,)
