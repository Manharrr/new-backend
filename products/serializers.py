# pyrefly: ignore [missing-import]
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
    # image = serializers.SerializerMethodField()  

    class Meta:
        model = Perfume
        fields = "__all__"

    # def get_image(self, obj):
    #     if not obj.image:
    #         return None
        
    #     try:
    #         # This might be '/media/https:/...' or 'https:/...' or 'perfumes/...'
    #         image_url = obj.image.url
    #     except Exception:
    #         return None
        
    #     # 1. If it's a corrupted path containing 'http' anywhere
    #     if 'http' in image_url:
    #         http_start = image_url.find('http')
    #         clean_url = image_url[http_start:]
            
    #         if 'https:/' in clean_url and 'https://' not in clean_url:
    #             clean_url = clean_url.replace('https:/', 'https://')
    #         elif 'http:/' in clean_url and 'http://' not in clean_url:
    #             clean_url = clean_url.replace('http:/', 'http://')
    #         return clean_url

    #     # 3. Handle local relative paths
    #     request = self.context.get("request")
    #     if request:
    #         return request.build_absolute_uri(image_url)
            
    #     return image_url