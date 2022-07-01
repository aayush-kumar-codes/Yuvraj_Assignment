from rest_framework import serializers
from drf_yasg import openapi

class RegisterField(serializers.JSONField):
    class Meta:
        swagger_schema_fields = {
            "type": openapi.TYPE_OBJECT,
            "title": "User Registration View",
            "properties": {
                "email": openapi.Schema(
                    title="email",
                    type=openapi.TYPE_STRING,
                ),
                "user_name": openapi.Schema(
                    title="username",
                    type=openapi.TYPE_STRING,
                ),
                "first_name": openapi.Schema(
                    title="First name",
                    type=openapi.TYPE_STRING,
                ),
                "last_name": openapi.Schema(
                    title="Last name",
                    type=openapi.TYPE_STRING,
                ),
                "gender": openapi.Schema(
                    title="Gender",
                    type=openapi.TYPE_STRING,
                ),
                "age": openapi.Schema(
                    title="Age",
                    type=openapi.TYPE_INTEGER,
                ),
                "country": openapi.Schema(
                    title="Country",
                    type=openapi.TYPE_INTEGER,
                ),
                "city": openapi.Schema(
                    title="city",
                    type=openapi.TYPE_INTEGER,
                ),
                "password": openapi.Schema(
                    title="Password",
                    type=openapi.TYPE_STRING,
                ),
                "confirm_password": openapi.Schema(
                    title="Confirm Password",
                    type=openapi.TYPE_STRING,
                ),
            },
            "required": ["email", "user_name", "first_name", "last_name", "gender", "age", "country", "city", "password", "confirm_password"],
        }