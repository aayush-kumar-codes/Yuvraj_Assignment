from rest_framework import serializers
from users.models import NewUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = '__all__'


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id', 'user_name', "first_name", "last_name",
                  "email", "gender", "age", "country", "city"]
