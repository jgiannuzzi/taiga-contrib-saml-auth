from django.conf.urls import patterns, url

from . import views

app_name = 'taiga_contrib_saml_auth'

urlpatterns = patterns('',
    url(r'^initiate-login/$', views.initiate_login, name="login_initiate"),
    url(r'^complete-login/$', views.complete_login, name="login_complete"),
    url(r'^initiate-logout/$', views.initiate_logout, name="logout_initiate"),
    url(r'^complete-logout/$', views.complete_logout, name="logout_complete"),
    url(r'^metadata/$', views.metadata, name="metadata"),
)
