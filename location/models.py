from django.db import models
from django.utils.translation import gettext_lazy as _

class Country(models.Model):
    country_code = models.CharField(max_length=3, unique=True, verbose_name=_("Country Code"))
    country_name = models.CharField(max_length=50, verbose_name=_("Country"))

    def __str__(self) -> str:
        return self.country_name


class City(models.Model):
    country = models.ForeignKey(to=Country, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=50, verbose_name=_("City"))

    def __str__(self) -> str:
        return self.city_name
