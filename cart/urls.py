from django.urls import path
from .views import AddToCart, UserCartView, UpdateCart, DeleteCart

urlpatterns = [
    path('add/', AddToCart.as_view()),
    path('view/', UserCartView.as_view()),
    path('update/<int:item_id>/', UpdateCart.as_view()),
    path('delete/<int:item_id>/', DeleteCart.as_view()),
]