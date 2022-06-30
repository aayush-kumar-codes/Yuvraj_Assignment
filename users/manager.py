from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class NewUserManager(BaseUserManager):

    """
        Custom user manager
    """

    def create_user(self, email, user_name, first_name, last_name, gender, age, country=None, city=None, password=None, **extra_fields):

        """creates a new user in the db"""
        if not email:
            raise ValueError(_('Email must be provided'))

        email = self.normalize_email(email)
        user = self.model(email=email, user_name=user_name,
                          first_name=first_name, gender=gender, age=age, **extra_fields)

        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, user_name, first_name, last_name, gender, age, password, **extra_fields):

        """creates a superuser"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Superuser must be assigned is_staff=True")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Superuser must be assigned is_superuser=True")

        return self.create_user(email, user_name, first_name, last_name, gender, age, password=password, **extra_fields)
