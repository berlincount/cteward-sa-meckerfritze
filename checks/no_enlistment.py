
def check_member(member_raw):
    if not member_raw['Eintritt']:
        return (False, "member enlistment never started")
    return (True,)
