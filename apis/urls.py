from rest_framework.routers import DefaultRouter

from location.api_v1.views import ListLocationViewSet, UploadCities
from sales.api_v1.views import SalesViewSet, SalesUploadView, StatisticsView
from users.api_v1.views import LogoutView, RegisterView, LoginView, UserActionView

from django.urls import path

router = DefaultRouter()

router.register(prefix=r'countries', viewset=ListLocationViewSet, basename='countries')
router.register(prefix=r'sales', viewset=SalesViewSet, basename='sales')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('users/<int:id>/', UserActionView.as_view(), name='user_action'),
    path('upload/', SalesUploadView.as_view(), name='sales_upload'),
    path('sales_statistics/', StatisticsView.as_view(), name='sales_statistics'),
    path('upload_cities/', UploadCities.as_view())


]

urlpatterns += router.urls