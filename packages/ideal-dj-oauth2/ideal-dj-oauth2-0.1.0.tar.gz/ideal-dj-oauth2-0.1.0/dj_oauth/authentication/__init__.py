# Initialize the authentication module
from .google import GoogleBackend
from .apple import AppleBackend
from .facebook import FacebookBackend
from .linkedin import LinkedInBackend

__all__ = [
    'GoogleBackend',
    'AppleBackend',
    'FacebookBackend',
    'LinkedInBackend'
]
