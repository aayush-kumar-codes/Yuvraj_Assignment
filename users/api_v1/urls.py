from django.urls import path

from .views import LoginView, RegisterView, UserActionView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view(), name='login'),
    path('<int:id>/', UserActionView.as_view())
]