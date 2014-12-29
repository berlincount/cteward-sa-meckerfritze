
def check(members_raw, check='duplicate_numbers'):
    members_by_number = {}
    duplicates = []
    for member_raw in members_raw:
        if member_raw['AdrNr'] in members_by_number:
            duplicates.append(member_raw['AdrNr'])
        else:
            members_by_number[member_raw['AdrNr']] = member_raw

    return (len(duplicates) == 0, duplicates)
