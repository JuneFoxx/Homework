from django.urls import path
from .views import page, products, first_page, json_get, index, about, contacts, gallery


app_name = "pages"

urlpatterns = [
    path('contacts/', contacts, name="contacts"),
    path('', index, name='index'),
    path('gallery', gallery, name='gallery'),
    path('about', about, name='about'),
    path('<int:id>/', products, name='product'),
    path('first_page/', first_page, name='first_page'),
    path('json_get/', json_get, name='json_get')
]
