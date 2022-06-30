from location.models import Country
from .serializers import CountrySerializer

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny

class ListLocationViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
