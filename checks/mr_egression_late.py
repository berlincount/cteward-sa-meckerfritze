import dateutil.parser
import datetime
import pytz

def check(member_raw, contracts=None, debits=None, withdrawals=None, name='egression_late'):
    if member_raw['Austritt'] and dateutil.parser.parse(member_raw['Austritt']) > datetime.datetime.now(pytz.timezone('Europe/Berlin'))+datetime.timedelta(weeks=56):
        return (False, "member discharged in more than a year")
    return (True,)
