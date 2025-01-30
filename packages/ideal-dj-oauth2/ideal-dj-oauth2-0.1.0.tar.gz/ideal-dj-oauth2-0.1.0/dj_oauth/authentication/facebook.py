from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import requests

User = get_user_model()

class FacebookBackend(BaseBackend):
    def authenticate(self, request, token=None):
    """
    Authenticate a Facebook user using the provided token.

    The token should be obtained after a Facebook login flow and is used
    to verify the user's identity via the Facebook Graph API.

    This method will validate the token, extract the user's email from
    Facebook, and create a new user in the database if the user does not
    already exist.

    :param request: The current request object
    :param token: The Facebook-provided access token
    :return: The authenticated user, or None if authentication failed
    """

        try:
            # Verify the Facebook token
            app_id = 'your_facebook_app_id'
            app_secret = 'your_facebook_app_secret'
            url = f'https://graph.facebook.com/debug_token?input_token={token}&access_token={app_id}|{app_secret}'
            response = requests.get(url)
            data = response.json()
            
            if 'error' in data['data']:
                return None
            
            # Get user information from Facebook
            user_info_url = f'https://graph.facebook.com/me?access_token={token}&fields=id,name,email'
            user_info_response = requests.get(user_info_url)
            user_info = user_info_response.json()
            
            email = user_info.get('email')
            if not email:
                return None
            
            user, created = User.objects.get_or_create(email=email)
            
            if created:
                user.username = user_info['name']
                user.save()
            
            return user
        except Exception:
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
