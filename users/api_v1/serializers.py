from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from users.models import NewUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'    

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    class Meta:
        model = NewUser
        fields = ['email','password']


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id', 'user_name', "first_name", "last_name",
                  "email", "gender", "age", "country", "city"]
