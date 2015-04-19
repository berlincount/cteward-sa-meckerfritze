# -*- coding: utf-8 -*-

# 7;Firmenmitglied;m;2011;1;170

def check_member(member_raw, contracts_raw):
    if member_raw["Betreung"] == "WEIBLICH" or member_raw["Betreung"] == "MÄNNLICH":
        return (True,)
    if all(int(contract_raw["Art"]) == 7 and contract_raw["ArtName"] == "Firmenmitglied" for contract_raw in contracts_raw):
        return (True,)
    return (False, "no business contract");
