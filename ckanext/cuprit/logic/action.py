from ckan.common import _
from ckan.logic.action.create import package_create as core_package_create
from ckan.logic.action.update import package_update as core_package_update
import ckan.plugins.toolkit as toolkit
from ckan import authz

import ckanext.cuprit.logic.auth_utils as auth_utils
import json

from logging import getLogger
log = getLogger(__name__)

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
    if auth_utils.is_user_editor_of_pkg_org(context, data_dict):
        data_dict['private'] = 'True'
    context["with_capacity"] = False

    return core_package_update(context, data_dict)

@toolkit.side_effect_free
def get_conf(context,data_dict=None):
    is_logged_in = authz.auth_is_loggedin_user()
    if not is_logged_in:
        return {}
  
    max_size = toolkit.config.get("ckan.max_resource.size")
    # TODO: refactor read path from settings
    ext_file = open('/srv/app/src/ckanext-cuprit/ckanext/cuprit/public/allowed_extensions.json')
    ext = json.load(ext_file)
    return {
        "max_size": max_size,
        "ext": ext['allowed_extensions']
    }
