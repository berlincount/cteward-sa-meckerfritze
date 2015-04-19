import dateutil.parser
import datetime
import pytz

def check_member(member_raw):
    if member_raw['Eintritt'] and dateutil.parser.parse(member_raw['Eintritt']) > datetime.datetime.now(pytz.timezone('Europe/Berlin'))+datetime.timedelta(weeks=56):
        return (False, "member enlistment starts in more than a year")
    return (True,)
