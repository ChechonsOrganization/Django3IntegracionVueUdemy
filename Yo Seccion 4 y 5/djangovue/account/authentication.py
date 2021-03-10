# importar usuario
from django.contrib.auth.models import User

# login via email

# una clase para personalizacion de la autenticación backend
class AuthByEmailBackend:

    def authenticate(self, request, username=None, password=None):
        # verificar si el usuario existe
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None