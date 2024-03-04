import distutils

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from ckan.common import config

import ckanext.cuprit.mailer as mailer
import ckanext.cuprit.logic.auth as auth
import ckanext.cuprit.logic.action as action
import ckanext.cuprit.lib.helpers as helpers
from ckanext.cuprit.lib.build_metadata_dict_dai import build_metadata_dict_dai
from ckanext.cuprit.lib.build_xml_dict_doi import build_xml_dict_doi
from flask import Blueprint
import ckanext.cuprit.blueprints as cuprit_blueprints
from ckan.lib.plugins import DefaultTranslation
from ckanext.cuprit.lib.choices import resource_types, get_custom_tags

from ckanext.doi.interfaces import IDoi


class CupritPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm, DefaultTranslation):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IAuthFunctions)
    plugins.implements(plugins.IActions)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IPackageController, inherit=True)
    # plugins.implements(plugins.IRoutes)
    plugins.implements(plugins.IFacets)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(IDoi, inherit=True)

    def _get_config_value(self, key):
        if config.get(key):
            if config.get(key).lower() in ['true', 'false']:
                return bool(distutils.util.strtobool(config.get(key)))
            else:
                return config.get(key)
        else:
            return ''

    def _modify_create_package_schema(self, schema):
        options = {
            'default': [toolkit.get_validator('ignore_missing'),
                        toolkit.get_converter('convert_to_extras')],
            'force_extras': [toolkit.get_validator('ignore_missing'),
                        toolkit.get_converter('convert_to_extras'),
                        toolkit.get_validator('not_empty')],
            'force_default': [toolkit.get_validator('not_empty')],
        }

        schema.update({
            'title': options.get('force_default'),
            'subtitle': options.get('default'),
            'notes': options.get('default'),
            'funding': options.get('default'),
            'version': options.get('force_default'),
            'license_id': options.get('force_default'),
            'notes': options.get('force_default'),
            'author': options.get('force_default'),
            'maintainer': options.get('force_default'),
            'maintainer_email': options.get('force_default'),
            'publisher': options.get('force_extras'),
            'contributor': options.get('default'),
            'ror_id': options.get('default'),
            'orcid_id': options.get('default'),
            'in_language': options.get('force_extras'),
            'year_of_publication': options.get('default'),
            'type_of_publication': options.get('force_extras'),
            'doi': options.get('default'),
            'related_resources': options.get('default'),
            'agree': options.get('default'),
        })
        
        return schema

    def _modify_show_package_schema(self, schema):
        options = {
            'default': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        }
        schema.update({
            'publisher': options.get('default'),
            'contributor': options.get('default'),
            'ror_id': options.get('default'),
            'in_language': options.get('default'),
            'year_of_publication': options.get('default'),
            'type_of_publication': options.get('default'),
            'doi': options.get('default'),
            'funding': options.get('default'),
            'subtitle': options.get('default'),
            'related_resources': options.get('default'),
            'agree': options.get('default'),
        })
        return schema


    # IConfigurer
    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'cuprit')
            
    # IDatasetForm
    def create_package_schema(self):
        schema = super(CupritPlugin, self).create_package_schema()
        schema = self._modify_create_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(CupritPlugin, self).update_package_schema()
        schema = self._modify_create_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(CupritPlugin, self).show_package_schema()
        schema = self._modify_show_package_schema(schema)
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
            'package_update': action.package_update,
            'get_conf': action.get_conf
        }
    
    # IFacets
    def _facets(self, facets_dict):
        if 'groups' in facets_dict:
            del facets_dict['groups']
        return facets_dict

    def dataset_facets(self, facets_dict, package_type):
        return self._facets(facets_dict)

    def group_facets(self, facets_dict, group_type, package_type):
        return self._facets(facets_dict)

    def organization_facets(self, facets_dict, organization_type,
            package_type):
        return self._facets(facets_dict)

    # ITemplateHelpers
    def get_helpers(self):
        '''
        Define custom helpers (or override existing ones).
        Available as h.{helper-name}() in templates.
        '''
        return {
            'is_editor': helpers.is_editor,
            'get_recent_articles': helpers.get_recent_articles,
            'resource_types': resource_types,
            'custom_tags': get_custom_tags(),
            'format_orcid': helpers.format_orcid,
            'format_resources': helpers.format_resources
        }

    # Custom pages
    def get_blueprint(self):
        # Create Blueprint for custom routes
        blueprint = Blueprint(self.name, self.__module__)
        blueprint.template_folder = u'templates'
        rules = [
            (u'/help', u'render_about_custom_page', cuprit_blueprints.render_about_custom_page),
        ]
        for rule in rules:
            blueprint.add_url_rule(*rule)

        return blueprint

    # IPackageController
    def after_create(self, context, pkg_dict):
        '''
        Called after a dataset has been created
        '''
        if self._get_config_value('ckanext.cuprit.email_sender'):
            mailer.mail_dataset_created_to_admins(context, pkg_dict)

    def build_metadata_dict(self, pkg_dict, metadata_dict, errors):
        """
        Customize DOI metadata dictionary
        """
        metadata_dict, errors = build_metadata_dict_dai(pkg_dict, metadata_dict, errors)
        return metadata_dict, errors


    def build_xml_dict(self, metadata_dict, xml_dict):
        """
        Customize DOI XML for datacite
        """
        xml_dict = build_xml_dict_doi(metadata_dict, xml_dict)
        return xml_dict

