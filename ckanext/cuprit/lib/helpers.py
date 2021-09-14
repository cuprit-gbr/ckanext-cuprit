import ckanext.cuprit.logic.authz as authz

def is_editor(user, office=None):
    """
    Returns True if user is editor of given organisation.
    If office param is not provided checks if user is editor of any organisation

    :param user: user name
    :type user: string
    :param office: office id
    :type office: string

    :returns: True/False
    :rtype: boolean
    """
    return authz.is_editor({'user': user}, {'user': user}, office)