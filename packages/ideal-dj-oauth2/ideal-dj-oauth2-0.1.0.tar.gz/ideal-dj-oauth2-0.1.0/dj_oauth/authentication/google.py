from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from google.oauth2 import id_token
from google.auth.transport import requests

User = get_user_model()

class GoogleBackend(BaseBackend):
    def authenticate(self, request, token=None):
        """
        Authenticate an Google user using the provided token.
        
        The token should be obtained after an Google login flow, and should be
        a JSON Web Token (JWT) signed by Google.
        
        The authenticate method will validate the token and extract the user's
        email from it. If a user with that email already exists in the database,
        that user will be returned. Otherwise, a new user will be created.
        
        :param request: The current request object
        :param token: The Google-provided JWT token
        :return: The authenticated user, or None if authentication failed
        """
        try:
            idinfo = id_token.verify_oauth2_token(token, requests.Request())
            
            if 'accounts.google.com' in idinfo['iss']:
                email = idinfo['email']
                user, created = User.objects.get_or_create(email=email)
                
                if created:
                    user.username = idinfo['name']
                    user.first_name = idinfo['given_name']
                    user.last_name = idinfo['family_name']
                    user.save()
                
                return user
        except ValueError:
            return None

    def get_user(self, user_id):
        """
        Retrieve a user by id.

        :param user_id: The id of the user to retrieve
        :return: The user with the given id, or None if no such user exists
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
