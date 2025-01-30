from django.conf import settings

# Define default roles and scopes
DEFAULT_ROLES = [
    'user',
    'admin',
    'advocate',
    'support'
]

DEFAULT_SCOPES = [
    'read',
    'write',
    'delete'
]

# Update settings to include custom OAuth and social account settings
CUSTOM_OAUTH_SETTINGS = {
    'USER_ROLES': getattr(settings, 'USER_ROLES', DEFAULT_ROLES),
    'USER_SCOPES': getattr(settings, 'USER_SCOPES', DEFAULT_SCOPES),
    'SOCIAL_AUTH': {
        'google': {
            'CLIENT_ID': getattr(settings, 'GOOGLE_CLIENT_ID', 'your_google_client_id'),
            'CLIENT_SECRET': getattr(settings, 'GOOGLE_CLIENT_SECRET', 'your_google_client_secret'),
        },
        'apple': {
            'CLIENT_ID': getattr(settings, 'APPLE_CLIENT_ID', 'your_apple_client_id'),
            'CLIENT_SECRET': getattr(settings, 'APPLE_CLIENT_SECRET', 'your_apple_client_secret'),
        },
        'facebook': {
            'CLIENT_ID': getattr(settings, 'FACEBOOK_CLIENT_ID', 'your_facebook_client_id'),
            'CLIENT_SECRET': getattr(settings, 'FACEBOOK_CLIENT_SECRET', 'your_facebook_client_secret'),
        },
        'linkedin': {
            'CLIENT_ID': getattr(settings, 'LINKEDIN_CLIENT_ID', 'your_linkedin_client_id'),
            'CLIENT_SECRET': getattr(settings, 'LINKEDIN_CLIENT_SECRET', 'your_linkedin_client_secret'),
        }
    },
    'DEFAULT_AUTH_METHODS': ['username', 'email', 'phone_number', 'google', 'apple', 'facebook', 'linkedin'],
}

# Merge custom settings with Django settings
settings.CUSTOM_OAUTH_SETTINGS = {**CUSTOM_OAUTH_SETTINGS, **getattr(settings, 'CUSTOM_OAUTH_SETTINGS', {})}
