# -*- coding: utf-8 -*-

# 7;Firmenmitglied;m;2011;1;170

def check(member_raw, contracts=None, debits=None, withdrawals=None, name='no_business_contract'):
    if member_raw["Betreung"] == "WEIBLICH" or member_raw["Betreung"] == "MÄNNLICH":
        return (True,)
    if all(int(contract["Art"]) == 7 and contract["ArtName"] == "Firmenmitglied" for contract in contracts):
        return (True,)
    return (False, "no business contract");
