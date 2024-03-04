from .clean_and_extract_orcid import clean_and_extract_orcid
from nameparser import HumanName
from ckanext.doi.lib import xml_utils

def build_xml_dict_doi(metadata_dict, xml_dict):
    print("Original XML dict:", xml_dict)

    # Ensure the 'resource' key exists in xml_dict
    if 'resource' not in xml_dict:
        xml_dict['resource'] = {}

    # Correctly handle creators
    processed_creators = []
    for creator_string in xml_dict.get('creators', []):
        # Assuming creator_string is a dict with 'name' and possibly other fields
        names = creator_string['name'].split(';')
        for name in names:
            cleaned_name, orcid = clean_and_extract_orcid(name)
            human_name = HumanName(cleaned_name)
            creator_dict = {
                'full_name': human_name.full_name,
                'family_name': human_name.last,
                'given_name': human_name.first,
                'is_org': False,
                'identifiers': [{'identifier': orcid, 'scheme': 'ORCID', 'scheme_uri': 'http://orcid.org'}] if orcid else []
            }
            processed_creators.append(creator_dict)
    xml_dict['creators'] = [xml_utils.create_contributor(**creator) for creator in processed_creators]

    # Process processed_contributors from metadata_dict
    xml_dict['contributors'] = []

    if 'processed_contributors' in metadata_dict:
        for contributor in metadata_dict['processed_contributors']:
            human_name = HumanName(contributor['name'])
            
            # Adjust the structure here to include 'name' key as expected by the schema
            contributor_dict = {
                'name': f"{human_name.first} {human_name.last}" if human_name.first and human_name.last else human_name.full_name,
                'contributorType': contributor['contributorType'],
            }
            
            # Including ORCID identifiers if available
            if contributor.get('orcid'):
                contributor_dict['nameIdentifiers'] = [{
                    'nameIdentifier': contributor['orcid'],
                    'nameIdentifierScheme': 'ORCID',
                    'scheme_uri': 'http://orcid.org',
                }]
            
            # Append this adjusted contributor dictionary
            xml_dict['contributors'].append(contributor_dict)

    print("New XML dict:", xml_dict)
    return xml_dict