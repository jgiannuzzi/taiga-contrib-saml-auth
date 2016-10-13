from django.conf import settings
from django.core.urlresolvers import reverse

def get_saml_settings():
    base_url = '{scheme}://{domain}'.format(
            scheme=settings.SITES['front']['scheme'],
            domain=settings.SITES['front']['domain'],
            )
    debug = settings.DEBUG

    saml_settings = {
            'strict': not debug,
            'debug': debug,
            'sp': {
                'entityId': base_url + reverse('taiga_contrib_saml_auth:metadata'),
                'assertionConsumerService': {
                    'url': base_url + reverse('taiga_contrib_saml_auth:login_complete'),
                    },
                'singleLogoutService': {
                    'url': base_url + reverse('taiga_contrib_saml_auth:logout_complete'),
                    },
                'NameIDFormat': settings.SAML_AUTH['sp'].get('nameIDFormat'),
                'x509cert': settings.SAML_AUTH['sp']['cert'],
                'privateKey': settings.SAML_AUTH['sp']['key'],
                },
            'idp': {
                'entityId': settings.SAML_AUTH['idp']['entityID'],
                'singleSignOnService': {
                    'url': settings.SAML_AUTH['idp']['singleSignOnURL'],
                    },
                'singleLogoutService': {
                    'url': settings.SAML_AUTH['idp']['singleLogoutURL'],
                    },
                },
            'security': settings.SAML_AUTH.get('security', {}),
            'organization': settings.SAML_AUTH.get('organization', {}),
            'contactPerson': settings.SAML_AUTH.get('contactPerson', {}),
            }

    if 'cert' in settings.SAML_AUTH['idp']:
        saml_settings['idp']['x509cert'] = settings.SAML_AUTH['idp']['cert']
    elif 'certFingerprint' in settings.SAML_AUTH['idp']:
        saml_settings['idp']['certFingerprint'] = settings.SAML_AUTH['idp']['certFingerprint']

    return saml_settings
