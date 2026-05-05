from rest_framework import serializers
from .models import Brand, Category, Perfume, Review


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ['user']


class PerfumeSerializer(serializers.ModelSerializer):
    reviews = ReviewSerializer(many=True, read_only=True)
    brand = BrandSerializer(read_only=True)     
    category = CategorySerializer(read_only=True)  

    class Meta:
        model = Perfume
        fields = "__all__"