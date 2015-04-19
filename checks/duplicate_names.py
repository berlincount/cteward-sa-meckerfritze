
def check_all(members_raw):
    members_by_name = {}
    duplicates = []
    for member_raw in members_raw:
        if member_raw['Kurzname'] in members_by_name:
            duplicates.append(member['Kurzname'])
        else:
            members_by_name[member_raw['Kurzname']] = member_raw

    return (len(duplicates) == 0, duplicates)
