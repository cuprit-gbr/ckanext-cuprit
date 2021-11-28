import ckan.logic as logic
import ckan.model as model
import ckan.plugins.toolkit as toolkit

from ckan.lib import base
from ckan.common import c

NotFound = logic.NotFound
ValidationError = logic.ValidationError

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

def is_user_editor_of_pkg_org(context, data_dict):
    model = context.get('model')
    user = context.get('user')

    name_or_id = data_dict.get('id') or data_dict.get('name')
    if name_or_id is None:
        raise ValidationError({'id': _('Missing value')})

    pkg = model.Package.get(name_or_id)
    if pkg is None:
        raise NotFound(_('Package was not found.'))

    return is_editor(context, user, pkg.owner_org)