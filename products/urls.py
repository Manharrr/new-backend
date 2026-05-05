from django.urls import path
from .views import (
    BrandListAPIView,
    BrandDetailAPIView,
    CategoryListAPIView,
    CategoryDetailAPIView,
    PerfumeListAPIView,
    PerfumeDetailAPIView,
    ReviewAPIView
)

urlpatterns = [

    # Brand
    path('brands/', BrandListAPIView.as_view()),
    path('brands/<int:pk>/', BrandDetailAPIView.as_view()),

    # Category
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view()),

    # Products
    path('perfumes/', PerfumeListAPIView.as_view()),
    path('perfumes/<int:pk>/', PerfumeDetailAPIView.as_view()),

    # Reviews
    path('reviews/', ReviewAPIView.as_view()),
]