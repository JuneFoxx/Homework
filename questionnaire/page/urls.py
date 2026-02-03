from django.urls import path
from . import views

app_name = "page"

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create_poll, name='create_poll'),
    path('<int:id>', views.get_poll_detailed, name='poll_id')
]