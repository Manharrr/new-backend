from rest_framework import serializers
from .models import Brand, Category, Perfume, PerfumeVariant, Review


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class PerfumeVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfumeVariant
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class PerfumeSerializer(serializers.ModelSerializer):
    variants = PerfumeVariantSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Perfume
        fields = "__all__"