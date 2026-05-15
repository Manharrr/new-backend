from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Brand, Category, Perfume, Review
from .serializers import (BrandSerializer,CategorySerializer,PerfumeSerializer,ReviewSerializer)
from django.db.models import Q


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
    
# class PerfumeListAPIView(APIView):
#     def get(self, request):
#         perfumes = Perfume.objects.all().select_related('brand', 'category').prefetch_related('reviews')
#         serializer = PerfumeSerializer(perfumes, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

class PerfumeListAPIView(APIView):
    def get(self, request):
        perfumes = Perfume.objects.all().select_related('brand', 'category').prefetch_related('reviews')

        category = request.query_params.get('category')
        if category:
            perfumes = perfumes.filter(category__name__iexact=category)


        search = request.query_params.get("search")
        if search:
            perfumes = perfumes.filter( Q(name__icontains=search) | Q(description__icontains=search))

        
        min_price = request.query_params.get("min_price")
        max_price = request.query_params.get("max_price")

        if min_price:
            perfumes = perfumes.filter(price__gte=min_price)
        if max_price:
            perfumes = perfumes.filter(price__lte=max_price)

        
        sort = request.query_params.get("sort")

        if sort == "asc":
            perfumes = perfumes.order_by("price")
        elif sort == "desc":
            perfumes = perfumes.order_by("-price")
        elif sort == "new":
            perfumes = perfumes.order_by("-created_at")

        serializer = PerfumeSerializer(perfumes,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PerfumeDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            perfume = Perfume.objects.get(pk=pk)
        except Perfume.DoesNotExist:
            return Response({"error": "Perfume not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PerfumeSerializer(perfume)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ReviewAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # def get(self, request):
    #     reviews = Review.objects.all()
    #     serializer = ReviewSerializer(reviews, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    def get(self, request):
        perfume_id = request.query_params.get("perfume")

        reviews = Review.objects.all()

        if perfume_id:
            reviews = reviews.filter(perfume_id=perfume_id)

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

