from django.db.models import Sum

from rest_framework.serializers import ModelSerializer, FileField

from sales.models import Sales


class SalesSerializer(ModelSerializer):
    class Meta:
        model = Sales
        fields = ['date', 'product', 'sales_number', 'revenue']


class SalesSerializerList(ModelSerializer):
    class Meta:
        model = Sales
        fields = '__all__'

class SalesUploadSerializer(ModelSerializer):
    csv_file = FileField()
    class Meta:
        model = Sales
        fields = ['csv_file',]
