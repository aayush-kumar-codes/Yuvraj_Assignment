from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from sales.stats import Stats
from .serializers import SalesSerializer, SalesSerializerList
from sales.models import Sales


class SalesUploadView(APIView):
    """
        view for uploading csv file data
    """

    def post(self, request):
        csv_file = request.FILES['csv_file']

        if not csv_file.name.endswith('.csv'):
            return Response(data={"detail": "The wrong file format was uploaded"})

        file_data = csv_file.read().decode("utf-8")
        csv_data = file_data.split("\n")[1:]

        for row in csv_data:
            fields = row.split(",")
            try:
                Sales.objects.create(
                    date=fields[0], product=fields[1], sales_number=fields[2], revenue=fields[3], user=request.user)
            except IndexError:
                pass

        return Response({"detail": "Data uploaded successfully"}, status=status.HTTP_201_CREATED)


class SalesViewSet(ViewSet):
    """
        contains all CRUD functionalities for Sales model
    """

    def list(self, request):
        queryset = Sales.objects.filter(user=request.user)
        serializer = SalesSerializerList(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            queryset = Sales.objects.get(user=request.user, pk=pk)
        except Sales.DoesNotExist:
            return Response({"detail": f"Sales data with id: {pk}, does not exists."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SalesSerializerList(queryset)
        return Response(serializer.data)

    def create(self, request):
        user = request.user
        serializer = SalesSerializerList(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def update(self, request, pk=None):
        try:
            queryset = Sales.objects.get(user=request.user, pk=pk)
        except Sales.DoesNotExist:
            return Response({"detail": f"Sales data with id: {pk}, does not exists."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SalesSerializer(instance=queryset, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors)

    def partial_update(self, request, pk=None):
        try:
            queryset = Sales.objects.get(user=request.user, pk=pk)
        except Sales.DoesNotExist:
            return Response({"detail": f"Sales data with id: {pk}, does not exists."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SalesSerializer(
            instance=queryset, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors)

    def destroy(self, request, pk=None):
        try:
            queryset = Sales.objects.get(user=request.user, pk=pk)
        except Sales.DoesNotExist:
            return Response({"detail": f"Sales data with id: {pk}, does not exists."}, status=status.HTTP_404_NOT_FOUND)

        queryset.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)


class StatisticsView(APIView):
    def get(self, request):
        sales_queryset = Sales.objects.all()
        stats = Stats(request=request, sales=sales_queryset)

        average_sales_for_current_user = stats.average_sales_for_user()
        avergae_sale_all_user = stats.average_sales_for_all_user()
        highest_revenue = stats.highest_sales_revenue()
        product_highest_sales = stats.product_highest_sales()

        response = {
            "average_sales_for_current_user": average_sales_for_current_user,
            "avergae_sale_all_user": avergae_sale_all_user,
            "highest_revenue_sale_for_current_user": {
                "sale_id": highest_revenue['sale_id'],
                "revenue": highest_revenue['max_revenue']
            },
            "product_highest_revenue_for_current_user": {
                "product_name": highest_revenue['product'],
                "sales_number": highest_revenue['sales_number']
            },
            "product_highest_sales_for_current_user": {
                "product_name": product_highest_sales['product'],
                "sales_number": product_highest_sales['sales_number']
            }
        }

        return Response(data=response, status=status.HTTP_200_OK)
