import dateutil.parser
import datetime

def check_member(member_raw, contracts_raw):
    if member_raw['Austritt'] and len(contracts_raw) and contracts_raw[len(contracts_raw)-1]['VertragEnde'] and dateutil.parser.parse(member_raw['Austritt'])+datetime.timedelta(days=21) < dateutil.parser.parse(contracts_raw[len(contracts_raw)-1]['VertragEnde']):
        return (False, "last contract of member ends more than 21 days before egression")
    return (True,)
