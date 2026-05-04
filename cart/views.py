# from django.shortcuts import render

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated



# class AddToCartAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         variant_id = request.data.get('variant')

#         try:
#             quantity = int(request.data.get('quantity', 1))
#         except:
#             return Response({"error": "Invalid quantity"})

#         try:
#             variant = PerfumeVariant.objects.get(id=variant_id)
#         except PerfumeVariant.DoesNotExist:
#             return Response({"error": "Variant not found"})

#         if quantity <= 0:
#             return Response({"error": "Invalid quantity"})

#         cart, _ = Cart.objects.get_or_create(user=user)

#         item, created = CartItem.objects.get_or_create(
#             cart=cart,
#             variant=variant
#         )

#         new_quantity = item.quantity + quantity if not created else quantity

#         if new_quantity > variant.stock:
#             return Response({"error": "Out of stock"})

#         item.quantity = new_quantity
#         item.save()

#         return Response({"msg": "Added to cart"})
    
# class UpdateCartItemAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def patch(self, request, pk):
#         try:
#             item = CartItem.objects.get(
#                 pk=pk,
#                 cart__user=request.user
#             )
#         except CartItem.DoesNotExist:
#             return Response({"error": "Item not found"})

#         try:
#             quantity = int(request.data.get('quantity'))
#         except:
#             return Response({"error": "Invalid quantity"})

#         if quantity <= 0:
#             return Response({"error": "Invalid quantity"})

#         if quantity > item.variant.stock:
#             return Response({"error": "Out of stock"})

#         item.quantity = quantity
#         item.save()

#         return Response({"msg": "Updated"})

# class RemoveCartItemAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, pk):
#         try:
#             item = CartItem.objects.get(
#                 pk=pk,
#                 cart__user=request.user
#             )
#         except CartItem.DoesNotExist:
#             return Response({"error": "Item not found"})

#         item.delete()
#         return Response({"msg": "Removed"})