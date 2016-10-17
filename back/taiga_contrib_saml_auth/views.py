from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings

from .settings import get_saml_settings

import logging
logger = logging.getLogger(__name__)


def get_saml_auth(request):
    return OneLogin_Saml2_Auth(
            {
                'https': 'on' if request.is_secure() else 'off',
                'http_host': request.META['HTTP_HOST'],
                'script_name': request.META['PATH_INFO'],
                'server_port': 443 if request.is_secure() else 80,
                'get_data': request.GET.copy(),
                'post_data': request.POST.copy(),
                },
            get_saml_settings(),
            )


@require_http_methods(['GET'])
def initiate_login(request):
    auth = get_saml_auth(request)
    return_url = request.GET.get('next', '/login')
    return HttpResponseRedirect(auth.login(return_to=return_url))


@csrf_exempt
@require_http_methods(['POST'])
def complete_login(request):
    auth = get_saml_auth(request)
    auth.process_response()
    errors = auth.get_errors()

    if errors:
        logger.error(auth.get_last_error_reason(), exc_info=True)
        return HttpResponseBadRequest(
                content='Error when processing SAML Response: {}'.format(', '.join(errors))
                )

    if auth.is_authenticated():
        request.session['saml_attributes'] = auth.get_attributes()
        request.session['saml_nameid'] = auth.get_nameid()
        request.session['saml_session_index'] = auth.get_session_index()

        params = {'state': 'saml'}
        url = request.POST.get('RelayState', '/login')

        return HttpResponseRedirect(auth.redirect_to(url, parameters=params))

    else:
        raise PermissionDenied()


def initiate_logout(request):
    auth = get_saml_auth(request)
    return HttpResponseRedirect(auth.logout(
            name_id=request.session.get('saml_nameid'),
            session_index=request.session.get('saml_session_index'),
            ))


def complete_logout(request):
    auth = get_saml_auth(request)
    url = auth.process_slo(delete_session_cb=lambda: request.session.flush())
    errors = auth.get_errors()

    if errors:
        logger.error(auth.get_last_error_reason(), exc_info=True)
        return HttpResponseBadRequest(
                content='Error when processing SAML Logout Request: {}'.format(', '.join(errors))
                )

    params = {}
    if url:
        params['next'] = url

    return HttpResponseRedirect(auth.redirect_to('/logout', parameters=params))


@require_http_methods(['GET'])
def metadata(request):
    saml_settings = OneLogin_Saml2_Settings(get_saml_settings(), sp_validation_only=True)
    metadata = saml_settings.get_sp_metadata()
    errors = saml_settings.validate_metadata(metadata)

    if errors:
        return HttpResponseServerError(content=', '.join(errors))

    return HttpResponse(content=metadata, content_type='text/xml')
