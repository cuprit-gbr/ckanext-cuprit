import logging

from ckan import model
from ckan.common import config
from ckan.plugins import toolkit
from ckan.lib.mailer import mail_user
from ckan.lib.base import render
from ckan.logic.action.get import member_list

log = logging.getLogger(__name__)

def mail_dataset_created_to_admins(
                        context, data_dict, event='request', feedback=None):
    '''
    Sends an email to organization admin with request to publish dataset
    '''
    members = member_list(
        context=context,
        data_dict={'id': data_dict.get('owner_org')}
    )
    admin_ids = [i[0] for i in members if i[2] == 'Admin']
    for admin_id in admin_ids:
        user = model.User.get(admin_id)
        if user.email:
            subj = _email_subj(data_dict=data_dict, event='request')
            body = _email_body(data_dict, user, event='request')
            header = {'Content-Type': 'text/html; charset=UTF-8'}
            try:
                mail_user(user, subj, body, headers=header)
                log.debug('[email] Dataset publishing request email sent to {0}'.format(user.name))
            except:
                log.debug('[email] Dataset publishing request - Could not send email to {0}'.format(user.name))

def _email_subj(data_dict, object_type='package', event='request'):
    '''
    Formats an email subject
    '''
    if object_type == 'package':
        object_type_str = 'Package'

    return '[DAINST] {0} Publishing {1}: {2}'.format(object_type_str, event.capitalize(), data_dict.get('title') or data_dict.get('name'))

def _email_body(data_dict, user, event='request'):
    '''
    Formats an email body
    '''
    pkg_link = toolkit.url_for('dataset.read', id=data_dict['name'], qualified=True)
    return render('emails/package_publish_{0}.html'.format(event), {
        'admin_name': user.fullname or user.name,
        'site_title': config.get('ckan.site_title'),
        'site_url': config.get('ckan.site_url'),
        'package_title': data_dict.get('title'),
        'package_description': data_dict.get('notes', ''),
        'package_url': pkg_link
    })
