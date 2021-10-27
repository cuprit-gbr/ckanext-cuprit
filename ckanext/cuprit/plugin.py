import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.cuprit.mailer as mailer
import ckanext.cuprit.logic.auth as auth
import ckanext.cuprit.logic.action as action
import ckanext.cuprit.lib.helpers as helpers

from flask import Blueprint
import ckanext.cuprit.blueprints as cuprit_blueprints
from ckan.lib.plugins import DefaultTranslation

class CupritPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IPackageController, inherit=True)

    # Custom pages
    def get_blueprint(self):
        # Create Blueprint for custom routes
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        rules = [
            (u'/participate', u'render_about_custom_page', cuprit_blueprints.render_about_custom_page),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cuprit')


    # IAuthFunctions
    def get_auth_functions(self):
        return {
            'package_update': auth.package_update
        }

    # IActions
    def get_actions(self):
        '''
        Define custom functions (or override existing ones).
        Available via API /api/action/{action-name}
        '''
        return {
            'package_create': action.package_create,
            'package_update': action.package_update
        }

    # ITemplateHelpers
    def get_helpers(self):
        '''
        Define custom helpers (or override existing ones).
        Available as h.{helper-name}() in templates.
        '''
        return {
            'is_editor': helpers.is_editor,
            'get_recent_articles': helpers.get_recent_articles
        }

    # IPackageController
    def after_create(self, context, pkg_dict):
        '''
        Called after a dataset has been created
        '''
        mailer.mail_dataset_created_to_admins(context, pkg_dict)

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []
