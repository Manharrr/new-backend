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
# from rest_framework import serializers
# from .models import Order, OrderItem


# class OrderItemSerializer(serializers.ModelSerializer):
#     product_name = serializers.ReadOnlyField(source='perfume.name')
#     product_price = serializers.ReadOnlyField(source='perfume.price')

#     class Meta:
#         model = OrderItem
#         fields = ['perfume', 'product_name', 'quantity', 'price', 'product_price']
#         read_only_fields = ['price']


# class OrderSerializer(serializers.ModelSerializer):
#     items = OrderItemSerializer(many=True)

#     class Meta:
#         model = Order
#         fields = ['id', 'payment_method', 'address', 'total_amount', 'status', 'items']
#         read_only_fields = ['total_amount', 'status']

#     def create(self, validated_data):
#         items_data = validated_data.pop('items')
#         user = self.context['request'].user

#         order = Order.objects.create(user=user, **validated_data)

#         total = 0

#         for item in items_data:
#             perfume = item['perfume']
#             qty = item['quantity']

#             if perfume.stock < qty:
#                 raise serializers.ValidationError(f"{perfume.name} out of stock")

#             price = perfume.price
#             total += price * qty

#             perfume.stock -= qty
#             perfume.save()

#             OrderItem.objects.create(
#                 order=order,
#                 perfume=perfume,
#                 quantity=qty,
#                 price=price
#             )

#         order.total_amount = total
#         order.status = "PLACED"
#         order.save()

#         return order