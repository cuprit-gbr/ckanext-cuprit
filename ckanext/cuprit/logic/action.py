import ckan.logic as logic
from ckan.common import _
from ckan.logic.action.create import package_create as core_package_create
from ckan.logic.action.update import package_update as core_package_update

import ckanext.cuprit.logic.authz as authz

NotFound = logic.NotFound
ValidationError = logic.ValidationError

from logging import getLogger
log = getLogger(__name__)

def _is_user_editor_of_pkg_org(context, data_dict):
    model = context.get('model')
    user = context.get('user')

    name_or_id = data_dict.get('id') or data_dict.get('name')
    if name_or_id is None:
        raise ValidationError({'id': _('Missing value')})

    pkg = model.Package.get(name_or_id)
    if pkg is None:
        raise NotFound(_('Package was not found.'))

    return authz.is_editor(context, user, pkg.owner_org)

def package_create(context, data_dict):
    '''
    Cuprit override for package create.

    Set default visibility for editors.
    '''
    #make dataset private by default
    data_dict['private'] = 'True'
    context["with_capacity"] = False

    return core_package_create(context, data_dict)

def package_update(context, data_dict):
    '''
    Cuprit override for package update.

    Set default visibility for editors.
    '''
    #make dataset private by default if user is editor
    if _is_user_editor_of_pkg_org(context, data_dict):
        data_dict['private'] = 'True'
    context["with_capacity"] = False

    return core_package_update(context, data_dict)
