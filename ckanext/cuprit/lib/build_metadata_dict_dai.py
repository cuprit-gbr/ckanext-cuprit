from .clean_and_extract_orcid_rorid import clean_and_extract_orcid, clean_and_extract_rorid, clean_and_extract_contributor_type

def build_metadata_dict_dai(pkg_dict, metadata_dict, errors):
    print("------------------------------------| old package metadata", pkg_dict)

    # Process contributors
    contributors_str = pkg_dict.get('contributor', '')
    contributors = []
    if contributors_str:
        for contributor_str in contributors_str.split(';'):
            cleaned_name, orcid = clean_and_extract_orcid(contributor_str)
            cleaned_name, rorid = clean_and_extract_rorid(cleaned_name)
            cleaned_name, contributorType = clean_and_extract_contributor_type(cleaned_name)

            contributors.append({
                'name': cleaned_name,
                'orcid': orcid,
                'rorid': rorid,
                'contributorType': contributorType
            })

    # Add processed contributors to metadata_dict with a unique key to avoid naming conflicts
    metadata_dict['contributors_with_ror_and_orcid'] = contributors

    # Process authors
    author_str = pkg_dict.get('author', '')
    authors = []
    if author_str:
        for author_str in author_str.split(';'):
            cleaned_name, orcid = clean_and_extract_orcid(author_str)
            cleaned_name, rorid = clean_and_extract_rorid(cleaned_name)
            authors.append({
                'name': cleaned_name,
                'orcid': orcid,
                'rorid': rorid
            })

    # Add processed author to metadata_dict with a unique key to avoid naming conflicts
    metadata_dict['author_with_ror_and_orcid'] = authors

    print("------------------------------------| new package metadata", metadata_dict)

    return metadata_dict, errors
