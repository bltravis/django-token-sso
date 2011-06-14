from token_sso.models import Token
from django.contrib.auth.models import User
   
class TokenSSOBackend(object):
    
    def authenticate(self, token=None):
        if token:
            try:
                token_obj = Token.objects.get(token=token)
            except Token.DoesNotExist:
                return None
            if token_obj.is_valid():
                token_obj.used = True
                token_obj.save()
                return token.user
            else:
                return None
        else:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None