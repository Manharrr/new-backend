from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartItemSerializer
from products.models import Perfume
from rest_framework import status


class UserCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()

        serializer = CartItemSerializer(items, many=True)
        total = sum(item.perfume.price * item.quantity for item in items)

        return Response({
            "items": serializer.data,
            "total": total
        })


class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        perfume_id = request.data.get("perfume")
        quantity = int(request.data.get("quantity", 1))

        if not perfume_id:
            return Response({"error": "Perfume ID required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            perfume = Perfume.objects.get(id=perfume_id)
        except Perfume.DoesNotExist:
            return Response({"error": "Perfume not found"}, status=status.HTTP_404_NOT_FOUND)

        if quantity > perfume.stock:
            return Response({"error": "Not enough stock"}, status=status.HTTP_400_BAD_REQUEST)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            perfume=perfume
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        if item.quantity > perfume.stock:
            item.quantity = perfume.stock

        item.save()

        return Response(CartItemSerializer(item).data)


class UpdateCart(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)

            quantity = int(request.data.get("quantity", item.quantity))

            if quantity <= 0:
                item.delete()
                return Response({"msg": "Item removed"})

            if quantity > item.perfume.stock:
                return Response({"error": "Exceeds stock"}, status=status.HTTP_400_BAD_REQUEST)

            item.quantity = quantity
            item.save()

            return Response(CartItemSerializer(item).data)

        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)


class DeleteCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.delete()
            return Response({"msg": "Deleted"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

class ClearCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart.items.all().delete()
        return Response({"msg": "Cart cleared"})