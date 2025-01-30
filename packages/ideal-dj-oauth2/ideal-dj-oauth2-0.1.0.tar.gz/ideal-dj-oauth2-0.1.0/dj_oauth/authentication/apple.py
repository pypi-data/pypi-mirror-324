from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import jwt
import requests

User = get_user_model()

class AppleBackend(BaseBackend):
    def authenticate(self, request, token=None):
        """
        Authenticate an Apple user using the provided token.
        
        The token should be obtained after an Apple login flow, and should be
        a JSON Web Token (JWT) signed by Apple.
        
        The authenticate method will validate the token and extract the user's
        email and username from it. If a user with that email already exists in
        the database, that user will be returned. Otherwise, a new user will be
        created.
        
        :param request: The current request object
        :param token: The Apple-provided JWT token
        :return: The authenticated user, or None if authentication failed
        """
        try:
            # Get Apple's public keys
            apple_keys_url = "https://appleid.apple.com/auth/keys"
            response = requests.get(apple_keys_url)
            keys = response.json().get('keys')
            
            # Decode the token using Apple's keys
            decoded_token = None
            for key in keys:
                try:
                    decoded_token = jwt.decode(token, key, algorithms=["RS256"], audience="your_client_id", issuer="https://appleid.apple.com")
                    break
                except jwt.ExpiredSignatureError:
                    return None
                except jwt.InvalidTokenError:
                    continue
            
            if not decoded_token:
                return None
            
            # Extract user info from the decoded token
            email = decoded_token['email']
            user, created = User.objects.get_or_create(email=email)
            
            if created:
                user.username = decoded_token['sub']
                user.save()
            
            return user
        except Exception:
            return None

    def get_user(self, user_id):
    """
    Retrieve a user by their unique user ID.

    This method attempts to fetch a user object from the database using
    the provided user_id. If a user with the given ID does not exist,
    it returns None.

    :param user_id: The unique identifier of the user to retrieve.
    :return: The User object if found, otherwise None.
    """

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
