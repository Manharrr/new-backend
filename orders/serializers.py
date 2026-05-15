from rest_framework import serializers
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):

    perfume_name = serializers.ReadOnlyField(
        source='perfume.name'
    )

    perfume_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem

        fields = [
            'perfume',
            'perfume_name',
            'perfume_image',
            'quantity',
            'price',
        ]

    def get_perfume_image(self, obj):

        request = self.context.get("request")

        if obj.perfume.image:
            return request.build_absolute_uri(
                obj.perfume.image.url
            )

        return None

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'payment_method', 'address', 'total_amount', 'status', 'items', 'created_at']
