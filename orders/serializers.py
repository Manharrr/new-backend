from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='perfume.name')
    product_price = serializers.ReadOnlyField(source='perfume.price')

    class Meta:
        model = OrderItem
        fields = ['perfume', 'product_name', 'quantity', 'price', 'product_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'payment_method', 'address', 'total_amount', 'status', 'items', 'created_at']
