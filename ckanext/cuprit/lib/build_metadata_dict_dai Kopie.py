from .clean_and_extract_orcid_rorid import clean_and_extract_orcid, clean_and_extract_rorid

def build_metadata_dict_dai(pkg_dict, metadata_dict, errors):
    print("package metadata", pkg_dict)

    # Process contributors
    contributors_str = pkg_dict.get('contributor', '')
    contributors = []
    if contributors_str:
        for contributor_str in contributors_str.split(';'):
            cleaned_name, orcid = clean_and_extract_orcid(contributor_str)
            cleaned_name, rorid = clean_and_extract_rorid(cleaned_name)  # Use the cleaned name from ORCID extraction
            contributors.append({
                'name': cleaned_name,
                'orcid': orcid,
                'rorid': rorid,  # Add RORID to the dictionary
                'contributorType': 'Researcher'  # Assuming all are Researchers; adjust as necessary
            })

    # Add processed contributors to metadata_dict with a unique key to avoid naming conflicts
    metadata_dict['processed_contributors'] = contributors

    maintainer_name = pkg_dict.get('maintainer', '')
    if maintainer_name:
        cleaned_name, orcid = clean_and_extract_orcid(maintainer_name)
        cleaned_name, rorid = clean_and_extract_rorid(cleaned_name)  # Repeat RORID extraction for maintainers if needed
        # Assuming the maintainer might also have an ORCID or RORID
        maintainer_dict = {
            'name': cleaned_name,
            'orcid': orcid,
            'rorid': rorid,  # Add RORID for the maintainer as well
            'contributorType': 'DataManager'  # Designating maintainer as a DataManager
        }
        # Check if 'processed_contributors' already exists, if not, initialize it
        if 'processed_contributors' not in metadata_dict:
            metadata_dict['processed_contributors'] = []
        metadata_dict['processed_contributors'].append(maintainer_dict)

    return metadata_dict, errors
