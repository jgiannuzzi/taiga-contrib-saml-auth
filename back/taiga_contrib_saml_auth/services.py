from django.conf import settings
from django.db import transaction as tx
from django.db import IntegrityError
from django.utils.translation import ugettext as _

from django.apps import apps

from taiga.base.utils.slug import slugify_uniquely
from taiga.base import exceptions as exc
from taiga.auth.services import send_register_email
from taiga.auth.services import make_auth_response_data, get_membership_by_token
from taiga.auth.signals import user_registered as user_registered_signal


@tx.atomic
def saml_register(saml_id, user_attributes, token=None):
    auth_data_model = apps.get_model('users', 'AuthData')
    user_model = apps.get_model('users', 'User')

    try:
        # SAML user association exist?
        auth_data = auth_data_model.objects.get(key="saml", value=saml_id)
        user = auth_data.user
    except auth_data_model.DoesNotExist:
        try:
            # Is a there a user with the same email as the SAML user?
            user = user_model.objects.get(email=user_attributes['email'])
            auth_data_model.objects.create(user=user, key='saml', value=saml_id, extra={})
        except user_model.DoesNotExist:
            # Create a new user
            user_attributes['username'] = slugify_uniquely(user_attributes['username'], user_model, slugfield='username')
            user = user_model.objects.create(**user_attributes)
            auth_data_model.objects.create(user=user, key='saml', value=saml_id, extra={})

            send_register_email(user)
            user_registered_signal.send(sender=user.__class__, user=user)

    if token:
        membership = get_membership_by_token(token)

        try:
            membership.user = user
            membership.save(update_fields=['user'])
        except IntegrityError:
            raise exc.IntegrityError(_("This user is already a member of the project."))

    return user


def saml_mapping(request):
    id_mapping = settings.SAML_AUTH['mapping'].get('id')
    attribute_mappings = settings.SAML_AUTH['mapping']['attributes']

    saml_id = request.session['saml_nameid']
    saml_attributes = request.session['saml_attributes']

    if id_mapping:
        saml_id = saml_attributes[id_mapping][0]

    user_attributes = {}
    for user_attr, saml_attr in attribute_mappings.items():
        user_attributes[user_attr] = saml_attributes[saml_attr][0]

    return saml_id, user_attributes


def saml_login_func(request):
    token = request.DATA.get('token', None)

    saml_id, user_attributes = saml_mapping(request)

    user = saml_register(saml_id, user_attributes, token)

    data = make_auth_response_data(user)
    return data
