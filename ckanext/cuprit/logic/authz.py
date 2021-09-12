from ckan.lib import base
import ckan.model as model
from ckan.common import c
import ckan.plugins.toolkit as toolkit

def get_user(username):
    ''' Try to get the user from c, if possible, and fallback to using the DB '''
    if not username:
        return None
    # See if we can get the user without touching the DB
    try:
        if c.userobj and c.userobj.name == username:
            return c.userobj
    except AttributeError:
        # c.userobj not set
        pass
    except TypeError:
        # c is not available
        pass
    # Get user from the DB
    return model.User.get(username)

def is_editor(context, user, org=None):
    """
    Returns True if user is editor of given organisation.
    If office param is not provided checks if user is editor of any organisation
    """
    user_orgs = toolkit.get_action(
                'organization_list_for_user')(context,{'user': user})
    if org is not None:
        return any([i.get('capacity') == 'editor' \
                and i.get('id') == org for i in user_orgs])
    return any([i.get('capacity') == 'editor' for i in user_orgs])