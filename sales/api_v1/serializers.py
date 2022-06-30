from django.db.models import Sum

from rest_framework.serializers import ModelSerializer, SerializerMethodField, Serializer

from sales.models import Sales


class SalesSerializer(ModelSerializer):
    class Meta:
        model = Sales
        fields = ['date', 'product', 'sales_number', 'revenue']


class SalesSerializerList(ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'
