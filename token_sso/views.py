from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.sites.models import Site
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from django.template import RequestContext
from django.shortcuts import render_to_response
from token_sso.models import Token, SiteSSOSettings, UserSSOSettings
from token_sso.util import secure_required, gen_token
from token_sso.backend import authenticate

@secure_required    
@login_required
def auth_redirect(request):
    referrer_id = request.REQUEST.get('referrer_id', None)
    if referrer_id:
        next = request.REQUEST.get('next', '')
        try:
            referrer_site = Site.objects.get(pk=referrer_id)
        except Site.DoesNotExist:
            return HttpResponseBadRequest()
        if UserSSOSettings.objects.get(user=request.user).use_sso_all:
            pass
        else:
            try:
                UserSSOSettings.objects.get(user=request.user).sso_sites.get(id=referrer_site.id)
            except UserSSOSettings.DoesNotExist:
                if next:
                    return HttpResponseRedirect(reverse('token_sso-authorize-site')+'?next=%s' % next)
                else:
                    return HttpResponseRedirect(reverse('token_sso-authorize-site'))
        token_hash = gen_token(request.user, site)
        token = Token(user=request.user, site=referrer_site, token=token_hash)
        token.save()
        consumer_url = 'https://' + site.domain + SiteSSOSettings.objects.get(site=referrer_site).url
        if next:
            return HttpResponseRedirect('%s%s/?next=%s' % (consumer_url, token, next))
        else:
            return HttpResponseRedirect('%s%s' % (consumer_url, token))
    else:
        return HttpResponseBadRequest()

@secure_required
@login_required
def authorize_site(request):
    referrer_id = request.REQUEST.get('referrer_id', None)
    if referrer_id:
        if request.method == 'POST':
            if 'cancel' in request.POST:
                return HttpResponseRedirect(reverse('token_sso-auth-cancel'))
            elif 'authorize' in request.POST:
                try:
                    referrer_site = Site.objects.get(pk=referrer_id)
                except Site.DoesNotExist:
                    return HttpResponseBadRequest()
                sso_settings = SiteSSOSettings.objects.get(user=request.user)
                sso_settings.sso_sites.add(referrer_site)
                return HttpResponseRedirect(reverse('token_sso-auth-redirect'))
            else:
                return HttpResponseBadRequest() 
        else:
            return render_to_response('token_sso/authorize_site.html', locals(), context_instance=RequestContext(request))
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
        