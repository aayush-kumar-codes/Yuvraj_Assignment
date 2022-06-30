from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.serializers import ValidationError
from rest_framework.generics import RetrieveAPIView, UpdateAPIView, CreateAPIView
from rest_framework.status import (
    HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
)

from users.permissions import UpdateDetailPermission

from . import serializers
from users.models import NewUser
from users.validators import password_validator
from users.utils import normalize_validation_error
from .custom_swagger import RegisterField


class RegisterView(APIView):
    """ User Registeration view """

    permission_classes = [AllowAny]

    def get_serializer(self):
        return RegisterField()

    def post(self, request):

        password = request.data.get('password')
        confirm_password = request.data.get('confirm_password')
        country = request.data.get('country', None)
        city = request.data.get('city', None)

        if not country:
            return Response({"detail": "country field can't be empty"})

        if not city:
            return Response({"detail": "city field can't be empty"})

        try:
            password_validator(password, confirm_password)
        except ValidationError as error:
            return Response(data=normalize_validation_error(error))

        serializer = serializers.RegisterSerializer(data=request.data)

        # if data is valid, create user
        if serializer.is_valid():
            user = serializer.save(password=make_password(
                request.data.get('password')))

            if not user:
                return Response(data={"error": "true", "details": serializer.errors}, status=HTTP_400_BAD_REQUEST)

            token = Token.objects.create(user=user)

            return Response(data={"token": token.key, "user_id": user.id}, status=HTTP_201_CREATED)

        else:
            return Response(data=serializer.errors, status=HTTP_400_BAD_REQUEST)


class LoginView(CreateAPIView):
    """ User Login View """

    permission_classes = [AllowAny]
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password')

        if not email:
            return Response({"detail": "email field can't be empty"})

        try:
            instance = NewUser.objects.get(email=email)
        except NewUser.DoesNotExist:
            # if user doesn't exists
            return Response(data={"user": "user with this email doesn't exists"}, status=HTTP_404_NOT_FOUND)

        user = authenticate(email=instance.email, password=password)

        if user is not None:
            # if user authentication is successful
            try:
                token = Token.objects.get(user_id=user.id)
            except:
                token = Token.objects.create(user=user)
            return Response(data={"token": token.key, "user_id": user.id}, status=HTTP_200_OK)
        # If password is incorrect
        return Response(data={"password": "incorrect password"}, status=HTTP_400_BAD_REQUEST)


class UserActionView(RetrieveAPIView, UpdateAPIView):
    """
        user details retrieve and update view
    """
    # checks if the user wants to update detail is the owner of the profile
    permission_classes = [UpdateDetailPermission]
    
    queryset = NewUser.objects.all()
    serializer_class = serializers.UserDetailSerializer
    lookup_field = 'id'

class LogoutView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        return Response(data={"detail": "User Logged out successfully"}, status=HTTP_200_OK)
