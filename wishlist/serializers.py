from rest_framework import serializers
from .models import WishlistItem


class WishlistItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='perfume.name')
    product_price = serializers.ReadOnlyField(source='perfume.price')
    product_image = serializers.ImageField(source='perfume.image', read_only=True)

    class Meta:
        model = WishlistItem
        fields = ['id', 'perfume', 'product_name', 'product_price', 'product_image']