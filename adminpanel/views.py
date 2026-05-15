# adminpanel/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser

from django.shortcuts import get_object_or_404
from django.db.models import Sum

from django.contrib.auth import get_user_model

from products.models import Perfume
from orders.models import Order,OrderItem

from .serializers import ( AdminUserSerializer, AdminProductSerializer, AdminOrderSerializer
)

User = get_user_model()


class AllUserView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        users = User.objects.all()

        serializer = AdminUserSerializer(
            users,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UserView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        user = get_object_or_404(User, pk=pk)

        serializer = AdminUserSerializer(user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class EditUserView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        user = get_object_or_404(User, pk=pk)

        serializer = AdminUserSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


# =========================
# PRODUCTS
# =========================

class AllProductsView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        products = Perfume.objects.all()

        serializer = AdminProductSerializer(
            products,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class SingleProductView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request, pk):

        product = get_object_or_404(
            Perfume,
            pk=pk
        )

        serializer = AdminProductSerializer(product)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class AddProductView(APIView):

    permission_classes = [IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):

        serializer = AdminProductSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        print(serializer.errors)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class EditProductView(APIView):

    permission_classes = [IsAdminUser]

    parser_classes = [
        MultiPartParser,
        FormParser
    ]

    def patch(self, request, pk):

        product = get_object_or_404(
            Perfume,
            pk=pk
        )

        serializer = AdminProductSerializer(
            product,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():

            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class soft_delete_view(APIView):

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):

        product = get_object_or_404(
            Perfume,
            pk=pk
        )

        product.delete()

        return Response(
            {"message": "Product deleted"},
            status=status.HTTP_204_NO_CONTENT
        )


# =========================
# ORDERS
# =========================

class AllOrdersView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        orders = Order.objects.all()

        serializer = AdminOrderSerializer(
            orders,
            many=True
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class UpdateOrderStatusView(APIView):

    permission_classes = [IsAdminUser]

    def patch(self, request, pk):

        order = get_object_or_404(
            Order,
            pk=pk
        )

        order.status = request.data.get(
            "status",
            order.status
        )

        order.save()

        serializer = AdminOrderSerializer(order)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


# =========================
# DASHBOARD
# =========================

class DashboardRevenueView(APIView):

    permission_classes = [IsAdminUser]

    def get(self, request):

        total_orders = Order.objects.count()

        total_revenue = (
            Order.objects.aggregate(
                total=Sum("total_amount")
            )["total"] or 0
        )

        # total_products_sold = (
        #     OrderItem.objects.aggregate(
        #         total=Sum("quantity")
        #     )["total"] or 0
        # )
        top_selling_products = (
            OrderItem.objects
            .values("perfume__name")
            .annotate(total_sold=Sum("quantity"))
            .order_by("-total_sold")[:5]
        )

        total_products = Perfume.objects.count()

        total_users = User.objects.count()
        blocked_users= User.objects.filter(is_active=False)

        return Response({
            "total_orders": total_orders,
            "total_revenue": total_revenue,
            "total_products": total_products,
            "total_users": total_users,
            "top_products": list(top_selling_products),
            "blocked_users":blocked_users.count()
        })

























# from django.contrib.auth import get_user_model
# from django.db.models import Sum

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAdminUser
# from rest_framework import status
# from rest_framework.decorators import api_view

# from products.models import Perfume
# from orders.models import Order, OrderItem

# from .serializers import  AdminUserSerializer, AdminProductSerializer, AdminOrderSerializer

# from rest_framework.parsers import (
#     MultiPartParser,
#     FormParser
# )
# User = get_user_model()


# class AllUserView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):

#         users = User.objects.all()

#         serializer = AdminUserSerializer( users, many=True)

#         return Response(serializer.data)


# class UserView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request, pk):

#         try:
#             user = User.objects.get(id=pk)

#         except User.DoesNotExist:

#             return Response(
#                 {"error": "User not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = AdminUserSerializer(user)

#         return Response(serializer.data)


# class EditUserView(APIView):
#     permission_classes = [IsAdminUser]

#     def patch(self, request, pk):

#         try:
#             user = User.objects.get(id=pk)

#         except User.DoesNotExist:

#             return Response(
#                 {"error": "User not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = AdminUserSerializer(
#             user,
#             data=request.data,
#             partial=True
#         )

#         serializer.is_valid(  raise_exception=True)

#         serializer.save()

#         return Response(serializer.data)


# # ========================= PRODUCTS =========================

# class AllProductsView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):

#         products = Perfume.objects.filter( is_deleted=False)

#         serializer = AdminProductSerializer(
#             products,
#             many=True
#         )

#         return Response(serializer.data)


# class SingleProductView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request, pk):

#         try:
#             product = Perfume.objects.get(
#                 id=pk,
#                 is_deleted=False
#             )

#         except Perfume.DoesNotExist:

#             return Response(
#                 {"error": "Product not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = AdminProductSerializer(
#             product
#         )

#         return Response(serializer.data)


# class AddProductView(APIView):
#     permission_classes = [IsAdminUser]

#     parser_classes = [
#         MultiPartParser,
#         FormParser
#     ]

#     def post(self, request):

#         serializer = AdminProductSerializer(
#             data=request.data
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         serializer.save()

#         return Response(
#             serializer.data,
#             status=status.HTTP_201_CREATED
#         )


# class EditProductView(APIView):
#     permission_classes = [IsAdminUser]

#     def patch(self, request, pk):

#         try:
#             product = Perfume.objects.get(id=pk)

#         except Perfume.DoesNotExist:

#             return Response(
#                 {"error": "Product not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         serializer = AdminProductSerializer(
#             product,
#             data=request.data,
#             partial=True
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         serializer.save()

#         return Response(serializer.data)


# @api_view(['PATCH'])
# def soft_delete_view(request, pk):

#     try:
#         product = Perfume.objects.get(id=pk)

#     except Perfume.DoesNotExist:

#         return Response(
#             {"error": "Product not found"},
#             status=status.HTTP_404_NOT_FOUND
#         )

#     product.is_deleted = True
#     product.save()

#     return Response({
#         "message": "Product soft deleted successfully"
#     })


# # ========================= ORDERS =========================

# class AllOrdersView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):

#         orders = Order.objects.all().order_by(
#             "-created_at"
#         )

#         serializer = AdminOrderSerializer(
#             orders,
#             many=True
#         )

#         return Response(serializer.data)


# class UpdateOrderStatusView(APIView):
#     permission_classes = [IsAdminUser]

#     def patch(self, request, pk):

#         try:
#             order = Order.objects.get(id=pk)

#         except Order.DoesNotExist:

#             return Response(
#                 {"error": "Order not found"},
#                 status=status.HTTP_404_NOT_FOUND
#             )

#         order.status = request.data.get(
#             "status"
#         )

#         order.save()

#         serializer = AdminOrderSerializer(
#             order
#         )

#         return Response(serializer.data)


# # ========================= DASHBOARD =========================

# class DashboardRevenueView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):

#         total_users = User.objects.count()

#         total_orders = Order.objects.count()

#         total_revenue = Order.objects.filter(is_paid=True ).aggregate(total=Sum("total_amount"))["total"] or 0

#         top_products = OrderItem.objects.values(
#             "perfume__name"
#         ).annotate(
#             total_sold=Sum("quantity")
#         ).order_by(
#             "-total_sold"
#         )[:5]

#         return Response({

#             "total_users": total_users,

#             "total_orders": total_orders,

#             "total_revenue": total_revenue,

#             "top_products": top_products
#         })
