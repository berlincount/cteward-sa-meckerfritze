import dateutil.parser
import datetime

def check_member(member_raw, contracts_raw):
    if member_raw['Eintritt'] and len(contracts_raw) and contracts_raw[0]['VertragBegin'] and dateutil.parser.parse(member_raw['Eintritt'])+datetime.timedelta(days=21) < dateutil.parser.parse(contracts_raw[0]['VertragBegin']):
        return (False, "first contract of member starts more than 21 days after enlistment")
    return (True,)
