from django.urls import path
from .views import AddToWishlist, UserWishlistView, DeleteWishlistItem

urlpatterns = [
    path('add/', AddToWishlist.as_view()),
    path('view/', UserWishlistView.as_view()),
    path('delete/<int:item_id>/', DeleteWishlistItem.as_view()),
]