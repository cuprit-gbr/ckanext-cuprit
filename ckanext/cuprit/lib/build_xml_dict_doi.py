from .clean_and_extract_orcid_rorid import clean_and_extract_orcid, clean_and_extract_rorid
from nameparser import HumanName
from ckanext.doi.lib import xml_utils

def build_xml_dict_doi(metadata_dict, xml_dict):

   # authors aka creators
    processed_creators = []
    if 'author_with_ror_and_orcid' in metadata_dict:
        for creator in metadata_dict['author_with_ror_and_orcid']:

            full_name = creator['name']
            ror_id = creator['rorid']
            orcid_id = creator['orcid']
            human_name = HumanName(full_name)
            family_name=human_name.last
            given_name=human_name.first
        
            a_creator = {
                'name': f'{family_name}, {given_name}',
                'nameIdentifiers': [{
                    'nameIdentifier': f'https://orcid.org/{orcid_id}',
                    'nameIdentifierScheme': 'ORCID',
                    'schemeUri': 'http://orcid.org',
                }],
                'affiliation': [{  
                    'name': f'{ror_id}',
                    'affiliationIdentifier': f'https://ror.org/{ror_id}',
                    'affiliationIdentifierScheme': 'ROR',
                    'schemeUri': 'https://ror.org',
                }]
            }
            
            processed_creators.append(a_creator)
        xml_dict['creators'] = processed_creators


   # contributors
    processed_contributors = []
    if 'contributors_with_ror_and_orcid' in metadata_dict:
        for contributor in metadata_dict['contributors_with_ror_and_orcid']:
            full_name = contributor['name']
            ror_id = contributor['rorid']
            orcid_id = contributor['orcid']
            human_name = HumanName(full_name)
            family_name=human_name.last
            given_name=human_name.first
            contributorType = contributor['contributorType']
        
            a_contributor = {
                'name': f'{family_name}, {given_name}',
                'contributorType': contributorType,
                'nameIdentifiers': [{
                    'nameIdentifier': f'https://orcid.org/{orcid_id}',
                    'nameIdentifierScheme': 'ORCID',
                    'schemeUri': 'http://orcid.org',
                }],
                'affiliation': [{  
                    'name': f'{ror_id}',
                    'affiliationIdentifier': f'https://ror.org/{ror_id}',
                    'affiliationIdentifierScheme': 'ROR',
                    'schemeUri': 'https://ror.org',
                }]
            }
            
            processed_contributors.append(a_contributor)
        xml_dict['contributors'] = processed_contributors
        xml_dict['creators'] = processed_contributors

    print("New XML dict:", xml_dict)
    return xml_dict
