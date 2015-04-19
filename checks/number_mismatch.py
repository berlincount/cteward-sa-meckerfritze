
def check_member(member_raw):
    if member_raw['MITGLNR'] == None or int(member_raw['AdrNr']) != int(member_raw['MITGLNR']):
        mitglnr_int = 0 if member_raw['MITGLNR'] == None else int(member_raw['MITGLNR'])
        return (False, "%s != %s" % (member_raw['AdrNr'], mitglnr_int))
    return (True,)
