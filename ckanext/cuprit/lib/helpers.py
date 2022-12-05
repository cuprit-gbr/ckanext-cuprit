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
    link author to orcids if id is found
    """
    authors = authors.split(";")
    author_html_str = ""
    for author in authors:
        author_orcid = re.search('(\d{4}-\d{4}-\d{4}-\d{4})', author)
        author = re.sub('\s?\(.*?\)', '', author)
        full_author = f'<a href="https://orcid.org/{author_orcid.group()}" target="blank">{author}</a>' \
                        if author_orcid is not None \
                        else f'{author}'
        author_html_str += f'{full_author}<br>'
    
    return author_html_str

def format_resources(resources: str) -> str:
    resources_html_str = ""
    resources = resources.split(";")
    for resource in resources:
        resource = resource.replace('""', '')
        resource = resource.replace('\"', '')
        resource = resource.replace('\"\"', '')
        resources_html_str += f'{resource}<br>'
    return resources_html_str