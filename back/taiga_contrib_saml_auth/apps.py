from django.apps import AppConfig


class TaigaContribSAMLAuthAppConfig(AppConfig):
    name = 'taiga_contrib_saml_auth'
    verbose_name = 'Taiga contrib SAML auth App Config'

    def ready(self):
        from taiga.auth.services import register_auth_plugin
        from . import services
        register_auth_plugin('saml', services.saml_login_func)
