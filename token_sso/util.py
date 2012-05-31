from django.http import HttpResponseRedirect
def secure_required(reject_insecure=False):
    """Decorator makes sure URL is accessed over https."""
    
    if reject_insecure and not request.is_secure():#If request is sent over non-secure connection and request data is deemed sufficiently sensitive (login data, for example), reject request.
        return HttpResponseBadRequest()
    def _read_opts(func):
        def _wrapped_view_func(request, *args, **kwargs):
            if not request.is_secure():
                if getattr(settings, 'HTTPS_SUPPORT', True):
                    request_url = request.build_absolute_uri(request.get_full_path())
                    secure_url = request_url.replace('http://', 'https://')
                    return HttpResponseRedirect(secure_url)
            return view_func(request, *args, **kwargs)
        return _read_opts
    return _wrapped_view_func


from Crypto.Hash import SHA256
from Crypto import Random
import datetime
def gen_token(user, site):
    r = Random.new()
    tokenizer = SHA256.new()
    tokenizer.update(str(user)+str(datetime.datetime.now())+r.read(64))    
    return tokenizer.hexdigest()