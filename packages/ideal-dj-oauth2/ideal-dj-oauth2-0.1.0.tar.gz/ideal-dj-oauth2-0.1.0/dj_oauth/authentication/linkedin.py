from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import requests

User = get_user_model()

class LinkedInBackend(BaseBackend):
    def authenticate(self, request, token=None):
        """
        Authenticate a user using a LinkedIn token.

        The authenticate method will validate the token and extract the user's
        email and username from it. If a user with that email already exists in
        the database, that user will be returned. Otherwise, a new user will be
        created.

        :param request: The current request object
        :param token: The LinkedIn-provided token
        :return: The authenticated user, or None if authentication failed
        """
        try:
            # Get user info from LinkedIn
            linkedin_url = 'https://api.linkedin.com/v2/me'
            headers = {
                'Authorization': f'Bearer {token}',
                'X-Restli-Protocol-Version': '2.0.0'
            }
            response = requests.get(linkedin_url, headers=headers)
            user_info = response.json()
            
            email_url = 'https://api.linkedin.com/v2/emailAddress?q=members&projection=(elements*(handle~))'
            email_response = requests.get(email_url, headers=headers)
            email_info = email_response.json()
            email = email_info['elements'][0]['handle~']['emailAddress']
            
            user, created = User.objects.get_or_create(email=email)
            
            if created:
                user.username = user_info['localizedFirstName'] + user_info['localizedLastName']
                user.first_name = user_info['localizedFirstName']
                user.last_name = user_info['localizedLastName']
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
