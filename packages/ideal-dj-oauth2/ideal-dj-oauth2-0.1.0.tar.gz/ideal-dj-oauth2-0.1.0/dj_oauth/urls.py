from django.urls import path
from .views import (
    RegisterView, 
    LoginView, 
    LogoutView, 
    RefreshTokenView, 
    ForgotPasswordView, 
    ProfileView, 
    DeviceManagementView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('password/forgot/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('device/manage/', DeviceManagementView.as_view(), name='device_manage'),
]
