import re

def clean_and_extract_orcid(name_string):
    """
    Cleans the name string by removing the ORCID identifiers and extracting ORCID if present.
    """
    orcid_match = re.search(r"\((\d{4}-\d{4}-\d{4}-\d{4})\)", name_string)
    orcid = orcid_match.group(1) if orcid_match else None
    cleaned_name = re.sub(r"\(\d{4}-\d{4}-\d{4}-\d{4}\)", "", name_string).strip()
    return cleaned_name, orcid

def clean_and_extract_rorid(name_string):
    """
    Cleans the name string by removing the RORID identifiers and extracting RORID if present.
    """
    rorid_match = re.search(r"\[([0-9a-zA-Z]+)\]", name_string)
    rorid = rorid_match.group(1) if rorid_match else None
    cleaned_name = re.sub(r"\[[0-9a-zA-Z]+\]", "", name_string).strip()
    return cleaned_name, rorid

def clean_and_extract_contributor_type(name_string):
    """
    Cleans the name string by removing the RORID identifiers and extracting RORID if present,
    defaulting to 'Researcher' if no specific type is found.
    """
    contributor_type_match = re.search(r"\{([a-zA-Z]+)\}", name_string)
    contributor_type = contributor_type_match.group(1) if contributor_type_match else 'Researcher'
    cleaned_name = re.sub(r"\{([a-zA-Z]+)\}", "", name_string).strip()

    return cleaned_name, contributor_type
