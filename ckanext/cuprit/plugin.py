import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckanext.cuprit.logic.auth as auth
import ckanext.cuprit.logic.action as action
import ckanext.cuprit.lib.helpers as helpers

class CupritPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cuprit')
    
    # IDatasetForm
    def create_package_schema(self):
        schema = super(CupritPlugin, self).create_package_schema()
        # our custom field
        schema.update({
            'gazetteer_id': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        return schema
    
    def update_package_schema(self):
        schema = super(CupritPlugin, self).update_package_schema()
        # our custom field
        schema.update({
            'gazetteer_id': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        return schema
    
    def show_package_schema(self):
        schema = super(CupritPlugin, self).show_package_schema()
        schema.update({
            'gazetteer_id': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

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
            'is_editor': helpers.is_editor
        }
