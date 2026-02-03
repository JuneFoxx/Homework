from django.urls import path, re_path
from .views import page, products, first_page, json_get, ContactsCreateView, ContactsUpdateView, AboutView, IndexView, GalleryView, GalleryDetailView, ContactsDeleteView


app_name = "pages"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about', AboutView.as_view(), name='about'),
    path('contacts', ContactsCreateView.as_view(), name='contacts'),
    path('contacts/<int:pk>/edit', ContactsUpdateView.as_view(), name='contacts'),
    path('contacts/<int:pk>/delete', ContactsDeleteView.as_view(), name='contacts'),
    path('gallery', GalleryView.as_view(), name='gallery'),
    path('gallery/<slug:slug>', GalleryDetailView.as_view(), name='gallery_detail'),
    path('<int:id>/', products, name='product'),
    path('first_page/', first_page, name='first_page'),
    path('json_get/', json_get, name='json_get')
]
