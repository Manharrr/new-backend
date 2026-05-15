


from rest_framework import serializers
from django.contrib.auth import get_user_model

from products.models import Perfume, Brand, Category
from orders.models import Order, OrderItem

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"


class AdminProductSerializer(serializers.ModelSerializer):

    brand_name = serializers.ReadOnlyField(source="brand.name")
    category_name = serializers.ReadOnlyField( source="category.name" )

    class Meta:
        model = Perfume
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


class AdminOrderItemSerializer(serializers.ModelSerializer):

    perfume_name = serializers.ReadOnlyField( source="perfume.name")

    class Meta:
        model = OrderItem
        fields = "__all__"


class AdminOrderSerializer(serializers.ModelSerializer):

    user_email = serializers.ReadOnlyField(source="user.email")

    items = AdminOrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"