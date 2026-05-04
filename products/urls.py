from django.urls import path
from .views import *

urlpatterns = [
    path('brands/', BrandListCreateAPIView.as_view()),
    path('brands/<int:pk>/', BrandDetailAPIView.as_view()),

    path('categories/', CategoryListCreateAPIView.as_view()),

    path('perfumes/', PerfumeListCreateAPIView.as_view()),
    path('perfumes/<int:pk>/', PerfumeDetailAPIView.as_view()),

    path('variants/', PerfumeVariantAPIView.as_view()),
    path('reviews/', ReviewAPIView.as_view()),
]