from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

from .manager import NewUserManager

from location.models import Country, City


class NewUser(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ("male", "male"),
        ("female", "female"),
        ("other", "other")
    )

    email = models.EmailField(_('email address'), unique=True)
    user_name = models.CharField(max_length=150, unique=True, verbose_name=_("username"))
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    gender = models.CharField(max_length=8, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    country = models.ForeignKey(to=Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(to=City, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = NewUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name', 'gender', 'age']

    def __str__(self) -> str:
        return self.email
