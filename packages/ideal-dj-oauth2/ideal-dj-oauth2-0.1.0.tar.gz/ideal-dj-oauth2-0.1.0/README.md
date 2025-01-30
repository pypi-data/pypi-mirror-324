# dj-oauth

dj-oauth is a Django REST framework package that provides OAuth2.0 and social account management. It supports various user types and offers flexible authentication methods, including username, email, phone number with OTP, Google, Apple, Facebook, and LinkedIn.

## Features

- **User Management**: Handle different user types (users, admins, advocates, support) defined in Django settings.
- **Authentication**: Support for multiple authentication methods.
- **Endpoints**: Login, logout, refresh token, forgot password, profile management, and device management.
- **Database**: Use MySQL/PostgreSQL for user data and Redis for session management.
- **User Information**: Save required user information such as first name, last name, email, mobile number, age, and date of birth.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/dj-oauth.git
    cd dj-oauth
    ```

2. **Install the package**:
    ```bash
    pip install .
    ```

3. **Add `dj_oauth` to `INSTALLED_APPS` in your Django settings**:
    ```python
    INSTALLED_APPS = [
        ...
        'dj_oauth',
    ]
    ```

4. **Configure OAuth and social account settings in your Django settings**:
    ```python
    AUTHENTICATION_BACKENDS = (
        'dj_oauth.authentication.google.GoogleBackend',
        'dj_oauth.authentication.apple.AppleBackend',
        'dj_oauth.authentication.facebook.FacebookBackend',
        'dj_oauth.authentication.linkedin.LinkedInBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    DJ_OAUTH = {
        'USER_ROLES': ['user', 'admin', 'advocate', 'support'],
        'SOCIAL_AUTH': {
            'google': {
                'CLIENT_ID': 'your_google_client_id',
                'CLIENT_SECRET': 'your_google_client_secret',
            },
            'apple': {
                'CLIENT_ID': 'your_apple_client_id',
                'CLIENT_SECRET': 'your_apple_client_secret',
            },
            'facebook': {
                'CLIENT_ID': 'your_facebook_client_id',
                'CLIENT_SECRET': 'your_facebook_client_secret',
            },
            'linkedin': {
                'CLIENT_ID': 'your_linkedin_client_id',
                'CLIENT_SECRET': 'your_linkedin_client_secret',
            }
        },
        'DEFAULT_AUTH_METHODS': ['username', 'email', 'phone_number', 'google', 'apple', 'facebook', 'linkedin'],
    }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_db_name',
            'USER': 'your_db_user',
            'PASSWORD': 'your_db_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```

## Usage

1. **Run migrations to create the necessary database tables**:
    ```bash
    python manage.py migrate
    ```

2. **Create a superuser to access the admin interface**:
    ```bash
    python manage.py createsuperuser
    ```

3. **Start the Django development server**:
    ```bash
    python manage.py runserver
    ```

4. **Access the API endpoints**:
    - **Register**: `POST /register/`
    - **Login**: `POST /login/`
    - **Logout**: `POST /logout/`
    - **Refresh Token**: `POST /token/refresh/`
    - **Forgot Password**: `POST /password/forgot/`
    - **Profile**: `GET/PUT /profile/`
    - **Device Management**: `POST/DELETE /device/manage/`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

---

Feel free to customize this `README.md` file to better fit your project's specific needs. If you need any further assistance, just let me know! 🚀
