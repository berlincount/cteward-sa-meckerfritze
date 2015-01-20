
def check(member_raw, contracts=None, debits=None, withdrawals=None, name='no_enlistment'):
    if not member_raw['Eintritt']:
        return (False, "member enlistment never started")
    return (True,)
