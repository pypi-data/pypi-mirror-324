from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle user login.

        Args:
            request (Request): Django request object

        Returns:
            Response: Django response object
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            # Handle token creation and return response
            return Response({"detail": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Handle token revocation
        """
        Handle token revocation.

        Args:
            request (Request): Django request object

        Returns:
            Response: Django response object
        """
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)

class RefreshTokenView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Handle token refresh
        """
        Handle token refresh.

        Args:
            request (Request): Django request object

        Returns:
            Response: Django response object
        """
        return Response({"detail": "Token refreshed"}, status=status.HTTP_200_OK)

class ForgotPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Handle the forgot password process by sending a password reset link to the user's email.

        Args:
            request (Request): Django request object containing the user's email.

        Returns:
            Response: Django response object indicating the status of the password reset process.
        """

        email = request.data.get('email')
        # Handle password reset logic
        return Response({"detail": "Password reset link sent"}, status=status.HTTP_200_OK)

class ProfileView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class DeviceManagementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # Handle adding new device
        """
        Handle adding new device.

        Args:
            request (Request): Django request object containing device information.

        Returns:
            Response: Django response object indicating the status of adding the device.
        """
        return Response({"detail": "Device added"}, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        # Handle removing device
        """
        Handle removing device.

        Args:
            request (Request): Django request object containing device information.

        Returns:
            Response: Django response object indicating the status of removing the device.
        """
        return Response({"detail": "Device removed"}, status=status.HTTP_200_OK)
