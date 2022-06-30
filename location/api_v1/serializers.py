from rest_framework.serializers import ModelSerializer, SerializerMethodField, CharField

from location.models import Country, City


class CitySerializer(ModelSerializer):
    name = CharField(source="city_name")

    class Meta:
        model = City
        fields = ['id', 'name']


class CountrySerializer(ModelSerializer):
    name = CharField(source="country_name")
    cities = SerializerMethodField(method_name="get_cities")

    class Meta:
        model = Country
        fields = ['id', 'name', 'cities']

    def get_cities(self, obj):
        cities = City.objects.filter(country=obj)
        serializer = CitySerializer(cities, many=True)
        return serializer.data
