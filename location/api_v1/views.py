from location.models import Country , City
from .serializers import CountrySerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

class ListLocationViewSet(ModelViewSet):
    """Lists countries and cities"""
    permission_classes = [AllowAny]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer


class UploadCities(APIView):
    schema=None
    permission_classes = [AllowAny]
    def get(self, request):
        import json
        file=open("countries.json")
        print("JJJJJJJJJJJ",type(file))
        for data in json.load(file):
            response = requests.post(url="https://countriesnow.space/api/v0.1/countries/cities", json=({"country": data['name']}))
            try:
                country = Country.objects.create(country_name=data['name'], country_code=data['code'])

                json_data = response.json()['data']

                for data in json_data[0:20]:
                    City.objects.create(country=country, city_name=data)
            except:
                pass
        return Response({})