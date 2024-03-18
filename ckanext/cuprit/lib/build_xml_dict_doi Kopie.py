from .clean_and_extract_orcid_rorid import clean_and_extract_orcid, clean_and_extract_rorid
from nameparser import HumanName
from ckanext.doi.lib import xml_utils

def build_xml_dict_doi(metadata_dict, xml_dict):

    if 'resource' not in xml_dict:
        xml_dict['resource'] = {}

    processed_creators = []
    for creator_string in xml_dict.get('creators', []):
        names = creator_string['name'].split(';')
        for name in names:
            cleaned_name, orcid = clean_and_extract_orcid(name)
            cleaned_name, rorid = clean_and_extract_rorid(name)
            human_name = HumanName(cleaned_name)

            if rorid:
                creator_dict = xml_utils.create_contributor(
                    full_name=human_name.full_name,
                    family_name=human_name.last,
                    given_name=human_name.first,
                    is_org=False,
                    affiliations=[f"https://rorid.org/{rorid}", "abc"],
                    identifiers=[{'identifier': orcid, 'scheme': 'ORCID', 'scheme_uri': 'http://orcid.org'}] if orcid else []
                )
            else:
                creator_dict = xml_utils.create_contributor(
                    full_name=human_name.full_name,
                    family_name=human_name.last,
                    given_name=human_name.first,
                    is_org=False,
                    identifiers=[{'identifier': orcid, 'scheme': 'ORCID', 'scheme_uri': 'http://orcid.org'}] if orcid else []
                )   
            
            processed_creators.append(creator_dict)
    xml_dict['creators'] = processed_creators

    xml_dict['contributors'] = []
    if 'processed_contributors' in metadata_dict:
        for contributor in metadata_dict['processed_contributors']:
            cleaned_name, rorid = clean_and_extract_rorid(contributor['name'])
            cleaned_name, orcid = clean_and_extract_orcid(cleaned_name)
            rorid = contributor['rorid']
            orcid = contributor['orcid']
            print("here we go with", rorid, orcid, cleaned_name)
            print(contributor["orcid"])
            human_name = HumanName(cleaned_name)

            if rorid:
                contributor_dict = xml_utils.create_contributor(
                    full_name=human_name.full_name,
                    family_name=human_name.last,
                    given_name=human_name.first,
                    contributor_type=contributor['contributorType'],
                    affiliations=f"https://rorid.org/{rorid}",
                    identifiers=[{'nameIdentifier': id, 'nameIdentifierScheme': scheme, 'schemeURI': uri} for id, scheme, uri in ((orcid, 'ORCID', 'http://orcid.org'), (rorid, 'ROR', 'http://ror.org')) if id]
                )

            else:
                contributor_dict = xml_utils.create_contributor(
                    full_name=human_name.full_name,
                    family_name=human_name.last,
                    given_name=human_name.first,
                    contributor_type=contributor['contributorType'],
                    identifiers=[{'nameIdentifier': id, 'nameIdentifierScheme': scheme, 'schemeURI': uri} for id, scheme, uri in ((orcid, 'ORCID', 'http://orcid.org'), (rorid, 'ROR', 'http://ror.org')) if id]
                )

            # Including ORCID identifiers if available
            if contributor.get('orcid'):
                contributor_dict['nameIdentifiers'] = [{
                    'nameIdentifier': contributor['orcid'],
                    'nameIdentifierScheme': 'ORCID',
                    'scheme_uri': 'http://orcid.org',
                }]

            xml_dict['contributors'].append(contributor_dict)

    print("New XML dict:", xml_dict)
    return xml_dict
