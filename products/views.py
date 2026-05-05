from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Brand, Category, Perfume, Review
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    PerfumeSerializer,
    ReviewSerializer
)

class BrandListAPIView(APIView):
    def get(self, request):
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BrandDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            brand = Brand.objects.get(pk=pk)
        except Brand.DoesNotExist:
            return Response({"error": "Brand not found"}, status=404)

        serializer = BrandSerializer(brand)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=404)

        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PerfumeListAPIView(APIView):
    def get(self, request):
        perfumes = Perfume.objects.all().select_related('brand', 'category').prefetch_related('reviews')
        serializer = PerfumeSerializer(perfumes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PerfumeDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            perfume = Perfume.objects.get(pk=pk)
        except Perfume.DoesNotExist:
            return Response({"error": "Perfume not found"}, status=404)

        serializer = PerfumeSerializer(perfume)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        reviews = Review.objects.all()
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Login required"}, status=401)

        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from .models import Brand, Category, Perfume, Review
# from .serializers import (
#     BrandSerializer,
#     CategorySerializer,
#     PerfumeSerializer,
#     ReviewSerializer
# )


# class BrandListCreateAPIView(APIView):

#     def get(self, request):
#         brands = Brand.objects.all()
#         serializer = BrandSerializer(brands, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = BrandSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class BrandDetailAPIView(APIView):

#     def get_object(self, pk):
#         try:
#             return Brand.objects.get(pk=pk)
#         except Brand.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         brand = self.get_object(pk)
#         if not brand:
#             return Response({"error": "Brand not found"}, status=404)

#         serializer = BrandSerializer(brand)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         brand = self.get_object(pk)
#         if not brand:
#             return Response({"error": "Brand not found"}, status=404)

#         serializer = BrandSerializer(brand, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors)

#     def delete(self, request, pk):
#         brand = self.get_object(pk)
#         if not brand:
#             return Response({"error": "Brand not found"}, status=404)

#         brand.delete()
#         return Response({"msg": "deleted"})
    
# class CategoryListCreateAPIView(APIView):

#     def get(self, request):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors)


# class CategoryDetailAPIView(APIView):

#     def get_object(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         category = self.get_object(pk)
#         if not category:
#             return Response({"error": "Category not found"}, status=404)

#         serializer = CategorySerializer(category)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         category = self.get_object(pk)
#         if not category:
#             return Response({"error": "Category not found"}, status=404)

#         serializer = CategorySerializer(category, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors)

#     def delete(self, request, pk):
#         category = self.get_object(pk)
#         if not category:
#             return Response({"error": "Category not found"}, status=404)

#         category.delete()
#         return Response({"msg": "deleted"})

# class PerfumeListCreateAPIView(APIView):

#     def get(self, request):
#         perfumes = Perfume.objects.all().select_related('brand', 'category').prefetch_related('reviews')
#         serializer = PerfumeSerializer(perfumes, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PerfumeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors)
    
# class PerfumeDetailAPIView(APIView):

#     def get_object(self, pk):
#         try:
#             return Perfume.objects.get(pk=pk)
#         except Perfume.DoesNotExist:
#             return None

#     def get(self, request, pk):
#         perfume = self.get_object(pk)
#         if not perfume:
#             return Response({"error": "Perfume not found"}, status=404)

#         serializer = PerfumeSerializer(perfume)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         perfume = self.get_object(pk)
#         if not perfume:
#             return Response({"error": "Perfume not found"}, status=404)

#         serializer = PerfumeSerializer(perfume, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)

#         return Response(serializer.errors)

#     def delete(self, request, pk):
#         perfume = self.get_object(pk)
#         if not perfume:
#             return Response({"error": "Perfume not found"}, status=404)

#         perfume.delete()
#         return Response({"msg": "deleted"})
    
# class ReviewAPIView(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         reviews = Review.objects.all()
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)
#             return Response(serializer.data)

#         return Response(serializer.errors)