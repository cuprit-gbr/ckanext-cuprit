from .clean_and_extract_orcid import clean_and_extract_orcid

def build_metadata_dict_dai(pkg_dict, metadata_dict, errors):
    print("package metadata", pkg_dict)

    # Process creators if not already done
    # Assuming creators are processed similarly

    # Process contributors
    contributors_str = pkg_dict.get('contributor', '')
    contributors = []
    if contributors_str:
        for contributor_str in contributors_str.split(';'):
            cleaned_name, orcid = clean_and_extract_orcid(contributor_str)
            contributors.append({
                'name': cleaned_name,
                'orcid': orcid,
                'contributorType': 'Researcher'  # Assuming all are Researchers; adjust as necessary
            })

    # Add processed contributors to metadata_dict with a unique key to avoid naming conflicts
    metadata_dict['processed_contributors'] = contributors

    maintainer_name = pkg_dict.get('maintainer', '')
    if maintainer_name:
        cleaned_name, orcid = clean_and_extract_orcid(maintainer_name)
        # Assuming the maintainer does not have an ORCID in the name field
        # Adjust if your data structure includes ORCID IDs for maintainers
        maintainer_dict = {
            'name': cleaned_name,
            'orcid': orcid,
            'contributorType': 'DataManager'  # Designating maintainer as a DataManager
        }
        # Check if 'processed_contributors' already exists, if not, initialize it
        if 'processed_contributors' not in metadata_dict:
            metadata_dict['processed_contributors'] = []
        metadata_dict['processed_contributors'].append(maintainer_dict)

    return metadata_dict, errors