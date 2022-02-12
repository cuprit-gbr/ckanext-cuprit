from ckan.common import _
from ckan.logic.action.create import package_create as core_package_create
from ckan.logic.action.update import package_update as core_package_update
import ckan.plugins.toolkit as toolkit
from ckan import authz
import os
import ckan.lib.helpers as h

import ckanext.cuprit.logic.auth_utils as auth_utils

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

    created_dataset = core_package_create(context, data_dict)
    if created_dataset:
        h.flash_success("Thank you for creating a dataset. Admins will receive a notification to check and publish your dataset.")

    return created_dataset

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
    
    ## it looks this does not respect api auth with token ;(
    # is_logged_in = authz.auth_is_loggedin_user()
    # if not is_logged_in:
    #    return {}
  
    # toolkit.config.get("ckan.max_resource.size")
    # does not work so read from env by now
    max_size = os.getenv('CKAN__MAX_RESOURCE_SIZE', 200)
    
    ext_file = os.getenv('CKANEXT__RESOURCE_VALIDATION__TYPES_FILE',
                         '/srv/app/src/ckanext-cuprit/ckanext/cuprit/config/resource_types.json')
    try:
        read_ext_file = open(ext_file)
        ext_file_content = json.load(read_ext_file)
        return {
            "max_size": max_size,
            "ext": ext_file_content['allowed_extensions']
        }
    except:
        return {"error": "Cannot read ext file"}
