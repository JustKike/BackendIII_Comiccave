from datetime import timedelta
from email import message
from django.utils import timezone
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

    

class ExpiringTOkenAuthentication(TokenAuthentication):
    expired = False
# tiempo de expiracion
    def expires_in(self,token):
        time_elapsed = timezone.now() - token.created
        left_time = timedelta(seconds = settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time
# compara si el token a expirado
    def is_token_expired(self,token):
        return self.expires_in(token) < timedelta(seconds = 0)
# Verifica si el token a expirado
    def token_expire_handler(self,token):
        is_expire = self.is_token_expired(token)
        # si el token expiro
        if is_expire:
            self.expired = True
            user = token.user
            token.delete()
            # se puede incluir borrar sesiones
            # refrescando token
            token = self.get_model().objects.create(user = user)

        return is_expire,token

    def authenticate_credentials(self,key):
        message,token,user = None,None,None
        try:
            token = self.get_model().objects.select_related('user').get(key = key)
            user = token.user
        except self.get_model().DoesNotExist:
            message = 'Token invalido'
            self.exired = True
        # si el token no es nulo
        if token is not None:
            if not token.user.is_authenticated:
                message = 'Usuario no activo o eliminado.'

            is_expired = self.token_expire_handler(token)
            if is_expired:
                message = 'Su token ha expirado'
            
        return (user,token,message,self.expired)

