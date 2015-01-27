import dateutil.parser
import datetime

def check(member_raw, contracts=None, debits=None, withdrawals=None, name='contract_ends_early'):
    if member_raw['Austritt'] and len(contracts) and contracts[len(contracts)-1]['VertragEnde'] and dateutil.parser.parse(member_raw['Austritt'])-datetime.timedelta(days=21) > dateutil.parser.parse(contracts[len(contracts)-1]['VertragEnde']):
        return (False, "last contract of member ends more than 21 days before egression")
    return (True,)
