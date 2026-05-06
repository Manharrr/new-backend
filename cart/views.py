from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Cart, CartItem
from .serializers import CartItemSerializer


class UserCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.items.all()
        serializer = CartItemSerializer(items, many=True)
        return Response(serializer.data)


class AddToCart(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)

        perfume_id = request.data.get("perfume")
        quantity = int(request.data.get("quantity", 1))

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            perfume_id=perfume_id
        )

        if not created:
            item.quantity += quantity
        else:
            item.quantity = quantity

        item.save()

        return Response({"msg": "Added to cart"})


class UpdateCart(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.quantity = int(request.data.get("quantity", item.quantity))
            item.save()
            return Response({"msg": "Updated"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)


class DeleteCart(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user)
            item.delete()
            return Response({"msg": "Deleted"})
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)