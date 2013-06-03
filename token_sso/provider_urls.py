from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'sso/login/$', 'token_sso.views.generate_token', name='token_sso_login_provider'),
    url(r'sso/logout/$', 'token_sso.views.sso_logout', name='token_sso_logout_provider'),
)