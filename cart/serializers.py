from rest_framework import serializers
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='perfume.name')
    product_price = serializers.ReadOnlyField(source='perfume.price')
    product_image = serializers.ImageField(source='perfume.image', read_only=True)
    stock = serializers.ReadOnlyField(source='perfume.stock')
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            'id','perfume','product_name','product_price','product_image','quantity','stock','subtotal'
        ]

    def get_subtotal(self, obj):
        return obj.perfume.price * obj.quantity
    
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than 0")
        return value
    
    def validate(self, data):
        perfume = data.get('perfume')
        quantity = data.get('quantity')

        if perfume and quantity:
            if quantity > perfume.stock:
                raise serializers.ValidationError("Quantity exceeds stock")

        return data