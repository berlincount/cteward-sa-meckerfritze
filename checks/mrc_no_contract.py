def check(member_raw, contracts=None, debits=None, withdrawals=None, name='no_contract'):
    if contracts == None or len(contracts) == 0:
        return (False, "no contract");
    return (True,)
