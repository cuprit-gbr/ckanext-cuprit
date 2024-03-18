import ckanext.cuprit.logic.auth_utils as auth_utils
import ckan.plugins.toolkit as tk
import re


def is_editor(user: str, office: str =None) -> bool:
    """
    Returns True if user is editor of given organisation.
    If office param is not provided checks if user is editor of any organisation

    :param user: user name
    :param office: office id
    """
    return auth_utils.is_editor({'user': user}, {'user': user}, office)

def get_recent_articles() -> dict:
    """
    get recent updated packages for startpage
    """
    result = tk.get_action("package_search")({}, {"rows": 10, "sort": "metadata_modified desc"})
    return result["results"]

def format_orcid(authors: str) -> str:
    """
    Link author to ORCIDs and RORIDs if IDs are found, combining them within parentheses.
    Additionally, extracts and formats plain text inside curly braces.
    """
    authors = authors.split(";")
    author_html_str = ""
    for author in authors:
        author_orcid = re.search('(\d{4}-\d{4}-\d{4}-\d{4})', author)
        author_rorid = re.search('\[(.*?)\]', author)
        author_type = re.search('\{(.*?)\}', author)  # Search for text within curly braces
        
        # Clean author name from identifiers
        clean_author = re.sub('\s?\(.*?\)', '', author).strip()
        clean_author = re.sub('\s?\[.*?\]', '', clean_author).strip()
        clean_author = re.sub('\s?\{.*?\}', '', clean_author).strip()
        
        links = []
        if author_type:
            links.append(f'<span class="tag opacity-75">{author_type.group(1)}</span>')
        if author_orcid:
            links.append(f'<a href="https://orcid.org/{author_orcid.group()}" class="tag opacity-75" target="_blank">ORCID ID: {author_orcid.group()}</a>')
        if author_rorid:
            links.append(f'<a href="https://ror.org/{author_rorid.group(1)}" class="tag opacity-75" target="_blank">ROR ID: {author_rorid.group(1)}</a>')


        # Combine ORCID, RORID, and type with a space if all or some exist
        combined_links = ' '.join(links)
        
        # Append combined links to the author name if not empty
        if combined_links:
            author_with_links = f'{clean_author} {combined_links}'
        else:
            author_with_links = clean_author

        author_html_str += f'{author_with_links}<br>'
    
    return author_html_str

def format_resources(resources: str) -> str:
    resources = str(resources)
    resources = resources.replace('"','')
    re.sub('"', '', resources)
    resources_html_str = ''
    resources = resources.split(";")
    for resource in resources:
        resources_html_str += f'{resource}<br>'
    return resources_html_str