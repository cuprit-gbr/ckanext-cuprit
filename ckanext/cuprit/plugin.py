import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class CupritPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IDatasetForm)

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
