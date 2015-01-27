import dateutil.parser
import datetime

def check(member_raw, contracts=None, debits=None, withdrawals=None, name='contract_starts_late'):
    if member_raw['Eintritt'] and len(contracts) and contracts[0]['VertragBegin'] and dateutil.parser.parse(member_raw['Eintritt'])+datetime.timedelta(days=21) < dateutil.parser.parse(contracts[0]['VertragBegin']):
        return (False, "first contract of member starts more than 21 days after enlistment")
    return (True,)
