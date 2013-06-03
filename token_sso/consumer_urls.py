from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'token/(?P<token>\w+)/$', 'token_sso.views.validate_token', name='token_sso_login'),
)