Taiga contrib SAML auth
=======================

The Taiga plugin for SAML authentication.

Heavily based on [taiga-contrib-github-auth](https://github.com/taigaio/taiga-contrib-github-auth) and [django-saml-service-provider](https://github.com/KristianOellegaard/django-saml-service-provider).

Installation
------------
### Production env

#### Taiga Back

In your Taiga back python virtualenv install the pip package `taiga-contrib-saml-auth` with:

```bash
pip install taiga-contrib-saml-auth
```

Modify your `settings/local.py` and include the lines:

```python
INSTALLED_APPS += ["taiga_contrib_saml_auth"]

SAML_AUTH = {
    # Service Provider settings (yourself)
    'sp': {
        # 'entityId', 'assertionConsumerService' and 'singleLogoutService' will be set automatically.

        # Uncomment if you want to specify a NameIDFormat
        #'NameIDFormat': 'urn:oasis:names:tc:SAML:2.0:nameid-format:transient',

        # This is your own Service Provider certificate
        'x509cert': '''-----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----''',

        # This is your own Service Provider private key
        'privateKey': '''-----BEGIN RSA PRIVATE KEY-----
        ...
        -----END RSA PRIVATE KEY-----''',
    },

    #
    # For more options and detailed description see https://github.com/onelogin/python3-saml
    #
    # Identity Provider settings (your partner doing the authentication)
    # These settings can be found in their metadata
    'idp': {
        # Identifier of the IdP entity  (must be a URI)
        'entityId': 'YOUR_IDP_ENTITY_ID',

        # SSO endpoint info of the IdP. (Authentication Request protocol)
        "singleSignOnService": {
            # URL Target of the IdP where the Authentication Request Message
            # will be sent.
            "url": 'YOUR_IDP_SSO_URL',
            # SAML protocol binding to be used when returning the <Response>
            # message. OneLogin Toolkit supports the HTTP-Redirect binding
            # only for this endpoint.
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },
        # SLO endpoint info of the IdP.
        "singleLogoutService": {
            # URL Location of the IdP where SLO Request will be sent.
            "url": 'YOUR_IDP_SLO_URL',
            # SAML protocol binding to be used when returning the <Response>
            # message. OneLogin Toolkit supports the HTTP-Redirect binding
            # only for this endpoint.
            "binding": "urn:oasis:names:tc:SAML:2.0:bindings:HTTP-Redirect"
        },

        # use either cert OR certFingerprint
        # This is the Identity Provider certificate
        'x509cert': '''-----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----''',
        # This is the Identify Provider certificate fingerprint
        # (Generate it with: openssl x509 -in YOUR_IDP_CERTIFICATE -noout -fingerprint | cut -d'=' -f2 | tr -d : | tr A-Z a-z)
        #'certFingerprint': 'YOUR_IDP_CERTIFICATE_FINGERPRINT',
    },

    # Security settings
    'security': {
        # These are the defaults
        #'nameIdEncrypted': False,
        #'authnRequestsSigned': False,
        #'logoutRequestSigned': False,
        #'logoutResponseSigned': False,
        #'signMetadata': False,
        #'wantMessagesSigned': False,
        #'wantAssertionsSigned': False,
        #'wantNameId': True,
        #'wantAssertionsEncrypted': False,
        #'wantNameIdEncrypted': False,
        #'wantAttributeStatement': True,
        #'requestedAuthnContext': True,
    },

    'organization': {
        # Organization information template, the info in en_US lang is
        # recommended, add more if required.
        'en-US': {
            'name': 'organization',
            'displayname': 'Organization Name',
            'url': 'https://www.example.org/',
        },
    },

    'contactPerson': {
        # Contact information template, it is recommended to suply a
        # technical and support contacts.
        'technical': {
            'givenName': 'technical_name',
            'emailAddress': 'technical@example.com'
        },
        'support': {
            'givenName': 'support_name',
            'emailAddress': 'support@example.com'
        },
    },

    # Mapping between the SAML user and the Taiga user
    'mapping': {
        # Uncomment to use a specific attribute as the SAML ID to link the Taiga user and the SAML user
        # By default, the SAML NameID will be used
        #'id': 'SAML_ATTRIBUTE_NAME',

        # You need to define at least email, username and full_name
        # (username and full_name can map to the same SAML attribute, as the username will be derived as
        # a unique slug from the given attribute)
        'attributes': {
            'email': 'SAML_ATTRIBUTE_NAME_EMAIL',
            'username': 'SAML_ATTRIBUTE_NAME_USERNAME',
            'full_name': 'SAML_ATTRIBUTE_NAME_FULLNAME',
            # 'bio': 'SAML_ATTRIBUTE_NAME_BIO',
            # 'lang': 'SAML_ATTRIBUTE_NAME_LANG',
            # 'timezone': 'SAML_ATTRIBUTE_NAME_TIMEZONE',
        },
    },
}

```

Modify your `taiga/urls.py` and include these lines:

```python
##############################################
# SAML Auth
##############################################

urlpatterns += [url(r'^saml/', include('taiga_contrib_saml_auth.urls'))]
```

#### Taiga Front

Download in your `dist/plugins/` directory of Taiga front the `taiga-contrib-saml-auth` compiled code:

```bash
cd dist/
mkdir -p plugins
cd plugins
version=$(pip show taiga-contrib-saml-auth | awk '/^Version: /{print $2}')
curl https://github.com/jgiannuzzi/taiga-contrib-saml-auth/archive/${version}.tar.gz | tar xzf -
mv taiga-contrib-saml-auth-${version}/front/dist saml-auth
rm -rf taiga-contrib-saml-auth-${version}
```

Include in your `dist/conf.json` in the 'contribPlugins' list the value `"/plugins/saml-auth/saml-auth.json"`:

```json
...
    "contribPlugins": [
        (...)
        "/plugins/saml-auth/saml-auth.json"
    ]
...
```

Configure your nginx to forward /saml/ to the backend:

```nginx
...
  # SAML authentication
  location /saml {
    proxy_set_header Host $http_host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Scheme $scheme;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header X-Forwarded-Protocol $scheme;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_pass http://backend$request_uri;
    proxy_redirect off;
    client_max_body_size 16M;
  }
...
```

### Dev env

#### Taiga Back

Clone the repo and

```bash
cd taiga-contrib-saml-auth/back
workon taiga
pip install -e .
```

Modify `taiga-back/settings/local.py`. See "Production env -> Taiga Back" section for content:


Modify your `taiga/urls.py` and include these lines:

```python
##############################################
# SAML Auth
##############################################

urlpatterns += [url(r'^saml/', include('taiga_contrib_saml_auth.urls'))]
```

#### Taiga Front

After clone the repo link `dist` in `taiga-front` plugins directory:

```bash
cd taiga-front/dist
mkdir -p plugins
cd plugins
ln -s ../../../taiga-contrib-saml-auth/dist saml-auth
```

Include in your `dist/conf.json` in the 'contribPlugins' list the value `"/plugins/saml-auth/saml-auth.json"`:

```json
...
    "contribPlugins": [
        (...)
        "/plugins/saml-auth/saml-auth.json"
    ]
...
```

In the plugin source dir `taiga-contrib-saml-auth/front` run

```bash
npm install
```
and use:

- `gulp` to regenerate the source and watch for changes.
- `gulp build` to only regenerate the source.
