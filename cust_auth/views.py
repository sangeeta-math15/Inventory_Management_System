import logging
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializer import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)


class WelcomeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        logger.info("Welcome endpoint accessed.")
        return Response("Welcome to Inventory Management System App", status=status.HTTP_200_OK)


def uniform_response(status_code, message, data=None):
    return Response({
        "status": status_code,
        "message": message,
        "data": data
    }, status=status_code)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {serializer.data['username']} registered successfully.")
            return uniform_response(status.HTTP_201_CREATED, "user registered successfully", serializer.data)
        logger.warning("User registration failed due to invalid data.")

        return uniform_response(status.HTTP_400_BAD_REQUEST, "User registration failed due to invalid data.", serializer.errors)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = None
        if '@' in username:
            try:
                user = User.objects.get(email=username)
            except ObjectDoesNotExist:
                logger.warning(f"Login failed for email {username}: User does not exist.")
        if not user:
            user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            logger.info(f"User {username} logged in successfully.")
            return uniform_response(status.HTTP_200_OK, "User logged in successfully.", {
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            })
        logger.warning(f"Login failed for {username}: Invalid credentials.")
        return uniform_response(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            logger.info("User logged out successfully.")
            return uniform_response(status.HTTP_200_OK, "message': 'Successfully logged out.")
        except Exception as e:
            logger.error(f"Logout failed: {str(e)}")
            return uniform_response(status.HTTP_400_BAD_REQUEST, {'error': str(e)})
