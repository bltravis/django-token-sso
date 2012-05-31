from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.conf in import settings
from django.utils.translation import ugettext as _

SSO_TOKEN_EXPIRES = getattr(settings, SSO_TOKEN_EXPIRES, 5)

class Token(models.Model):
    """
    Model for storing one-time use authentication tokens for single-sign-on.
    """
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)
    token = models.CharField(max_length=64)
    created = models.DateTimeField(default=datetime.datetime.now))
    used_expired = models.BooleanField(default=False)
    
    def __unicode__(self):
        return 'SSO token for user: %s accessing site: %s' % (self.user, self.site)
    
    def is_valid(self):
        if self.site == Site.objects.get_current() and self.user.is_active() and not self.used:
            if datetime.datetime.now() > self.created + datetime.timedelta(seconds=SSO_TOKEN_EXPIRES):
                self.used_expired = True
                self.save()
                return False
            self.used_expired = True
            return True
        else:
            return False

class SignOnEvent(models.Model):
    user = models.ForeignKey(User)
    site = models.ForeignKey(Site)
    client_ip = models.IPAddressField()
    successful = models.BooleanField()
    event_date_time = models.DateTimeField(default=datetime.datetime.now)
    
    def __unicode__(self):
        if self.successful:
            return u'Successful SSO Event: %s(user), %s(site), %s(ip)' % (self.user, self.site, self.client_ip)
        else:
            return u'Failed SSO Event: %s(user), %s(site), %s(ip)' % (self.user, self.site, self.client_ip)
    
    
class SiteSSOSettings(models.Model):
    """
    Model for storing site-specific token auth consumer url information.
    """
    site = models.ForeignKey(Site)
    url = models.CharField(max_length=40, help_text=_("URL of the site's token auth consumer view."))
    
    def __unicode__(self):
        return 'Site SSO Settings for %s' % self.site.name

class UserSSOSettings(models.Model):
    """
    Model for storing user-specific SSO settings/preferences.
    """
    user = models.ForeignKey(User)
    use_sso_all = models.BooleanField(default=True)
    sso_sites = models.ManyToManyField(Site)
    sign_out_all = models.BooleanField(default=True)
    first_time_prompt = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u'SSO preferences for %s' % (self.user)
    