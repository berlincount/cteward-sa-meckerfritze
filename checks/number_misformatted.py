
def check_member(member_raw):
    if member_raw['MITGLNR'] == None or "%04d" % int(member_raw['MITGLNR']) != member_raw['MITGLNR']:
        mitglnr_formatted = 'None' if member_raw['MITGLNR'] == None else "%04d" % int(member_raw['MITGLNR'])
        return (False, "%s != %s" % (mitglnr_formatted, member_raw['MITGLNR']))
    return (True,)
