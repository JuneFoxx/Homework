from django.urls import path
from django.contrib.auth import urls
from .views import RegistrationView, LoginView, LogoutView

namespace = "users"

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]


