from django.urls import path
from .views import IndexView, SubscriptionCreateView, SubscriptionDeleteView, SubscriptionUpdateView, deactivate_subscription, ConfirmPaymentView

app_name = "pages"

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('add_subscription/', SubscriptionCreateView.as_view(), name='add_subscription'),
    path('subscription/<int:pk>/delete/', SubscriptionDeleteView.as_view(), name='subscription_delete'),
    path('subscription/<int:pk>/edit/', SubscriptionUpdateView.as_view(), name='subscription_edit'),
    path('deactivate_subscription/<int:pk>/', deactivate_subscription, name='deactivate_subscription'),
    path('confirm-payment/<int:pk>/', ConfirmPaymentView.as_view(), name='confirm_payment'),
]
