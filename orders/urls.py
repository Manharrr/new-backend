from django.urls import path
from .views import CreateOrderView, OrderHistoryView, CancelOrderView,BuyNowOrderView

urlpatterns = [
    path('create/', CreateOrderView.as_view()),
    path('history/', OrderHistoryView.as_view()),
    path('cancel/<int:order_id>/', CancelOrderView.as_view()),
    path('buy-now/', BuyNowOrderView.as_view()),
]
