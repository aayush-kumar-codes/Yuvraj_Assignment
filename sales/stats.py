from django.db.models import Sum, Max, Min

class Stats:
    """
        class Stats:
        contains methods for calculating sales statistics
    """
    def __init__(self, request, sales) -> None:
        self.request = request
        self.sales = sales


    def average_sales_for_user(self):
        """Divides the total revenue for all the sales by the number of sales for that user"""
        queryset = self.sales.filter(user=self.request.user)
        total_revenue = queryset.aggregate(Sum('revenue'))
        total_sales = queryset.aggregate(Sum('sales_number'))

        try:
            average_sales = (total_revenue['revenue__sum'] / total_sales['sales_number__sum'])
        except TypeError:
            average_sales = None
        return average_sales

    def average_sales_for_all_user(self):
        """Divide the total sales revenue for all users’ sales by the number of all sales"""
        queryset = self.sales
        total_revenue = queryset.aggregate(Sum('revenue'))
        total_sales = queryset.aggregate(Sum('sales_number'))

        try:
            average_sales = (total_revenue['revenue__sum'] / total_sales['sales_number__sum'])
        except TypeError:
            average_sales = None
        return average_sales

    def highest_sales_revenue(self):
        """ Get the product that has produced the highest total amount of revenue for the user"""
        queryset = self.sales.filter(user=self.request.user)
        obj = queryset.filter(revenue=queryset.aggregate(Max('revenue'))['revenue__max'])
        if len(obj) > 1:
            obj = obj.filter(sales_number=obj.aggregate(Min('sales_number'))['sales_number__min'])
        obj = obj.first()

        if not obj:
            return {'sale_id': None, 'max_revenue': None, 'product': None, 'sales_number': None}
        return {'sale_id': obj.id, 'max_revenue': obj.revenue, 'product': obj.product, 'sales_number': obj.sales_number}

    def product_highest_sales(self):
        """Get the product which the user has the largest number ofsales for"""
        queryset = self.sales.filter(user=self.request.user)
        obj = queryset.filter(sales_number=queryset.aggregate(Max('sales_number'))['sales_number__max']).first()
        if not obj:
            return {'product': None, 'sales_number': None}
        return {'product': obj.product, 'sales_number': obj.sales_number}

