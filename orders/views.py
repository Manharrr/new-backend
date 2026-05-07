from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from decimal import Decimal

from cart.models import CartItem
from .models import Order, OrderItem,Perfume
from .serializers import OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        user = request.user

        cart_items = CartItem.objects.filter(cart__user=user)

        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)

        order = Order.objects.create(
            user=user,
            address=request.data.get("address"),
            payment_method=request.data.get("payment_method", "COD")
        )

        total = Decimal("0.00")

        for item in cart_items:
            perfume = item.perfume
            qty = item.quantity

            if perfume.stock < qty:
                return Response(
                    {"error": f"{perfume.name} out of stock"},
                    status=400
                )

            price = perfume.price
            total += price * qty

            # reduce stock
            perfume.stock -= qty
            perfume.save()

            OrderItem.objects.create(
                order=order,
                perfume=perfume,
                quantity=qty,
                price=price
            )

        order.total_amount = total
        order.status = "PLACED"
        order.save()

        # clear cart
        cart_items.delete()

        return Response({
            "message": "Order placed successfully",
            "order_id": order.id,
            "total": total
        })


class OrderHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, user=request.user)

            if order.status in ["SHIPPED", "DELIVERED"]:
                return Response({"error": "Cannot cancel"}, status=400)

            order.status = "CANCELLED"
            order.save()

            return Response({"msg": "Order cancelled"})
        except Order.DoesNotExist:
            return Response({"error": "Not found"}, status=404)
        

class BuyNowOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        perfume_id = request.data.get("perfume")
        quantity = int(request.data.get("quantity", 1))

        perfume = Perfume.objects.get(id=perfume_id)

        if perfume.stock < quantity:
            return Response({"error": "Out of stock"}, status=400)

        order = Order.objects.create(
            user=request.user,
            address=request.data.get("address"),
            payment_method=request.data.get("payment_method", "COD")
        )

        total = perfume.price * quantity

        OrderItem.objects.create(
            order=order,
            perfume=perfume,
            quantity=quantity,
            price=perfume.price
        )

        # reduce stock
        perfume.stock -= quantity
        perfume.save()

        order.total_amount = total
        order.status = "PLACED"
        order.save()

        return Response({
            "message": "Buy Now order placed",
            "order_id": order.id
        })
        

# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Order
# from .serializers import OrderSerializer
# from rest_framework import status


# class CreateOrderView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = OrderSerializer(data=request.data, context={'request': request})

#         if serializer.is_valid():
#             order = serializer.save()
#             return Response({
#                 "message": "Order placed successfully",
#                 "order_id": order.id
#             })
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OrderHistoryView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         orders = Order.objects.filter(user=request.user).order_by('-created_at')
#         serializer = OrderSerializer(orders, many=True)
#         return Response(serializer.data)


# class CancelOrderView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, order_id):
#         try:
#             order = Order.objects.get(id=order_id, user=request.user)

#             if order.status in ["SHIPPED", "DELIVERED"]:
#                 return Response({"error": "Cannot cancel now"}, status=400)

#             order.status = "CANCELLED"
#             order.save()

#             return Response({"msg": "Order cancelled"})
#         except Order.DoesNotExist:
#             return Response({"error": "Not found"}, status=404)