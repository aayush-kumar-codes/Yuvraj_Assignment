from django.contrib import admin

from sales.models import Sales


class SalesAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'sales_number', 'revenue', 'date')


admin.site.register(Sales, SalesAdmin)
