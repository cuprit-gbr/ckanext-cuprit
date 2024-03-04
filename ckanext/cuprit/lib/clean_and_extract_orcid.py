import re

def clean_and_extract_orcid(name_string):
    """
    Cleans the name string by removing the ORCID identifiers and extracting ORCID if present.
    """
    orcid_match = re.search(r"\((\d{4}-\d{4}-\d{4}-\d{4})\)", name_string)
    orcid = orcid_match.group(1) if orcid_match else None
    cleaned_name = re.sub(r"\(\d{4}-\d{4}-\d{4}-\d{4}\)", "", name_string).strip()
    return cleaned_name, orcid