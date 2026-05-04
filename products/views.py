from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Brand
from .serializers import BrandSerializer


class BrandListCreateAPIView(APIView):

    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BrandSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class BrandDetailAPIView(APIView):

    def get_object(self, pk):
        return Brand.objects.get(pk=pk)

    def get(self, request, pk):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand)
        return Response(serializer.data)

    def put(self, request, pk):
        brand = self.get_object(pk)
        serializer = BrandSerializer(brand, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        brand = self.get_object(pk)
        brand.delete()
        return Response({"msg": "deleted"})
    
class CategoryListCreateAPIView(APIView):

    def get(self, request):
        data = Category.objects.all()
        serializer = CategorySerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    
class PerfumeListCreateAPIView(APIView):

    def get(self, request):
        perfumes = Perfume.objects.all().select_related('brand', 'category').prefetch_related('variants', 'reviews')
        serializer = PerfumeSerializer(perfumes, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PerfumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

class PerfumeDetailAPIView(APIView):

    def get_object(self, pk):
        return Perfume.objects.get(pk=pk)

    def get(self, request, pk):
        perfume = self.get_object(pk)
        serializer = PerfumeSerializer(perfume)
        return Response(serializer.data)

    def put(self, request, pk):
        perfume = self.get_object(pk)
        serializer = PerfumeSerializer(perfume, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def delete(self, request, pk):
        perfume = self.get_object(pk)
        perfume.delete()
        return Response({"msg": "deleted"})
    

class PerfumeVariantAPIView(APIView):

    def post(self, request):
        serializer = PerfumeVariantSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)
    

from rest_framework.permissions import IsAuthenticatedOrReadOnly

class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)