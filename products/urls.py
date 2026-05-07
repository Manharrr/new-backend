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
    path('brands/', BrandListAPIView.as_view()),
    path('brands/<int:pk>/', BrandDetailAPIView.as_view()),

    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view()),

    path('perfumes/', PerfumeListAPIView.as_view()),
    path('perfumes/<int:pk>/', PerfumeDetailAPIView.as_view()),

    path('reviews/', ReviewAPIView.as_view()),
]