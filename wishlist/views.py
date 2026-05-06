from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Wishlist, WishlistItem
from products.models import Perfume
from .serializers import WishlistItemSerializer


class AddToWishlist(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        perfume_id = request.data.get("perfume")

        if not perfume_id:
            return Response({"error": "perfume is required"}, status=400)

        try:
            perfume = Perfume.objects.get(id=perfume_id)
        except Perfume.DoesNotExist:
            return Response({"error": "Perfume not found"}, status=404)

        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)

        item = WishlistItem.objects.filter(wishlist=wishlist, perfume=perfume).first()

        #  Toggle behavior
        if item:
            item.delete()
            return Response({"msg": "Removed from wishlist"})

        item = WishlistItem.objects.create(wishlist=wishlist, perfume=perfume)
        serializer = WishlistItemSerializer(item)

        return Response(serializer.data, status=201)


class UserWishlistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
        items = wishlist.items.select_related("perfume")
        serializer = WishlistItemSerializer(items, many=True)

        return Response(serializer.data)


class DeleteWishlistItem(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = WishlistItem.objects.get(id=item_id, wishlist__user=request.user)
            item.delete()
            return Response({"msg": "Deleted"})
        except WishlistItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=404)