from rest_framework.routers import DefaultRouter

from location.api_v1.views import ListLocationViewSet
from sales.api_v1.views import SalesViewSet, SalesUploadView, StatisticsView
from users.api_v1.views import RegisterView, LoginView, UserActionView

from django.urls import path

router = DefaultRouter()

router.register(prefix=r'countries', viewset=ListLocationViewSet)
router.register(prefix=r'sales', viewset=SalesViewSet, basename='sales')

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('<int:id>/', UserActionView.as_view()),
    path('upload/', SalesUploadView.as_view()),
    path('sales_statistics/', StatisticsView.as_view())
]
