from rest_framework import status
from rest_framework.authentication import get_authorization_header
from django.contrib.messages import constants as messages
from .authentication import ExpiringTOkenAuthentication

class Autentication(object):
    user = None
    user_token_expired = False

    def get_user(self,request):
        token = get_authorization_header(request).split()
        if token:
            try:
                token = token[1].decode()
            except:
                return None
            token_expire = ExpiringTOkenAuthentication()
            user,token,message,self.user_token_expired = token_expire.authenticate_credentials(token)
            
            if user != None and token != None:
                self.user = user
                return user

            return message
            
        return None

    def dispatch(self, request, *args, **kwargs):
        user = self.get_user(request)
        #faund token in request
        if user is not None:
            if type(user) == str:
                messages.error(request,{'Error': user,'expired':self.user_token_expired},
                                            status = status.HTTP_400_BAD_REQUEST)

            if not self.user_token_expired:
                return super().dispatch(request, *args, **kwargs)

        messages.error(request,{'Error': 'No se han enviado las credenciales',
                                    'expired':self.user_token_expired},status = status.HTTP_400_BAD_REQUEST)