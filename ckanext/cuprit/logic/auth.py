import ckan.logic.auth as logic_auth
from ckan.logic.auth.update import package_update as core_package_update_auth

from ckanext.cuprit.logic.auth_utils import(
    get_user,
    is_editor
)

from logging import getLogger
log = getLogger(__name__)

def package_update(context, data_dict):
    result = core_package_update_auth(context, data_dict)

    username = context.get('user')
    package = logic_auth.get_package_object(context, data_dict)

    if not username:
        return result

    user = get_user(username=username)

    # check if user is owner of the dataset
    pkg_user_id = package.creator_user_id
    if pkg_user_id == user.id:
        return result

    if package.owner_org:
        if is_editor(context=context, user=username, org=package.owner_org):
            return {'success': False, 'msg': 'User not allowed to update the dataset.'}

    return result
