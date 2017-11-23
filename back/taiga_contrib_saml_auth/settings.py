from django.conf import settings
from django.core.urlresolvers import reverse


def get_saml_settings():
    base_url = '{scheme}://{domain}'.format(
        scheme=settings.SITES['front']['scheme'],
        domain=settings.SITES['front']['domain'],
    )
    debug = settings.DEBUG

    saml_settings = dict(settings.SAML_AUTH)

    saml_settings['strict'] = settings.SAML_AUTH.get('strict', not debug)
    saml_settings['debug'] = settings.SAML_AUTH.get('debug', debug)
    del(saml_settings['mapping'])
    saml_settings['sp'].update({
        'entityId': base_url + reverse('taiga_contrib_saml_auth:metadata'),
        'assertionConsumerService': {
            'url': base_url + reverse('taiga_contrib_saml_auth:login_complete'),
        },
        'singleLogoutService': {
            'url': base_url + reverse('taiga_contrib_saml_auth:logout_complete'),
        },
    })

    return saml_settings
