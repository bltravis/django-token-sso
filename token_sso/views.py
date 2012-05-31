from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from token_sso.models import Token, SiteSSOSettings
from token_sso.util import secure_required, gen_token
from token_sso.backend import authenticate

@secure_required    
@login_required
def auth_redirect(request, referrer_id=None):
    if referrer_id:
        try:
            site = Site.objects.get(pk=referrer_id)
        except Site.DoesNotExist:
            return HttpResponseBadRequest()
        token_hash = gen_token(request.user, site)
        token = Token(user=request.user, site=site, token=token_hash)
        token.save()
        consumer_url = 'https://' + site.domain + SiteSSOSettings.objects.get(site=site).url
        if request.REQUEST.has_key('next'):
            next = request.REQUEST['next']
            return HttpResponseRedirect('%s%s/?next=%s' % (consumer_url, token, next))
        else:
            return HttpResponseRedirect('%s%s' % (consumer_url, token))
    else:
        return HttpResponseBadRequest()
        
@secure_required
def auth_token_receiver(request, token):
    user = authenticate(token=token)
    if user is not None and user.is_active:
        login(request, user)
        next = request.REQUEST.get('next', '')
        if next:
            HttpRepsonseRedirect(next)
        else:
            HttpResponseRedirect(getattr(settings, 'LOGIN_REDIRECT_URL', '/'))
        