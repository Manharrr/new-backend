# adminpanel/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model

from products.models import Perfume, Brand, Category
from orders.models import Order, OrderItem


User = get_user_model()


# USER SERIALIZER
class AdminUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"
# PRODUCT SERIALIZER

class AdminProductSerializer(serializers.ModelSerializer):

    brand_name = serializers.ReadOnlyField(
        source="brand.name"
    )

    category_name = serializers.ReadOnlyField(
        source="category.name"
    )

    class Meta:
        model = Perfume
        fields = "__all__"


# =========================================================
# BRAND SERIALIZER
# =========================================================

class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = "__all__"


# =========================================================
# CATEGORY SERIALIZER
# =========================================================

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = "__all__"


# =========================================================
# ORDER ITEM SERIALIZER
# =========================================================

class AdminOrderItemSerializer(
    serializers.ModelSerializer
):

    perfume_name = serializers.ReadOnlyField(
        source="perfume.name"
    )

    class Meta:
        model = OrderItem
        fields = "__all__"


# =========================================================
# ORDER SERIALIZER
# =========================================================

class AdminOrderSerializer(
    serializers.ModelSerializer
):

    user_email = serializers.ReadOnlyField(
        source="user.email"
    )

    items = AdminOrderItemSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = Order
        fields = "__all__"