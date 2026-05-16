import razorpay

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from cart.models import CartItem
from .models import Payment

from .serializers import (
    PaymentSerializer,
    CreatePaymentSerializer,
    VerifyPaymentSerializer)


class CreatePaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreatePaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order_id = serializer.validated_data["order_id"]

        try:
            order = Order.objects.get(
                id=order_id,
                user=request.user
            )
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=404)

        if order.is_paid:
            return Response({"message": "Order already paid"})

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        razorpay_order = client.order.create({
            "amount": int(order.total_amount * 100),
            "currency": "INR",
            "payment_capture": 1
        })

        payment, created = Payment.objects.get_or_create(
            order=order,
            defaults={
                "amount": order.total_amount,
                "razorpay_order_id": razorpay_order["id"]
            }
        )

        if not created:
            payment.razorpay_order_id = razorpay_order["id"]
            payment.save()

        serializer = PaymentSerializer(payment)

        return Response({
            "payment": serializer.data,
            "razorpay_order_id": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "key": settings.RAZORPAY_KEY_ID
        })


class VerifyPaymentView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = VerifyPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        client = razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET
            )
        )

        try:
            client.utility.verify_payment_signature({
                "razorpay_order_id": data["razorpay_order_id"],
                "razorpay_payment_id": data["razorpay_payment_id"],
                "razorpay_signature": data["razorpay_signature"]
            })

            payment = Payment.objects.get(
                razorpay_order_id=data["razorpay_order_id"]
            )

            if payment.status == "SUCCESS":
                return Response({"message": "Payment already completed"})

            payment.razorpay_payment_id = data["razorpay_payment_id"]
            payment.razorpay_signature = data["razorpay_signature"]
            payment.status = "SUCCESS"
            payment.save()

            order = payment.order
            order.is_paid = True
            order.status = "PLACED"   
            order.save()

            # Stock update
            for item in order.items.all():
                perfume = item.perfume

                if perfume.stock < item.quantity:
                    return Response({
                        "error": f"{perfume.name} out of stock"
                    }, status=400)

                perfume.stock -= item.quantity
                perfume.save()

            #  KEY FIX: Buy Now aanel cart clear cheyyilla
            # Cart checkout (is_buy_now=False) aanel mathram clear cheyyunnu
            if not order.is_buy_now:
                CartItem.objects.filter(cart__user=order.user).delete()

            return Response({"message": "Payment successful"})

        except Exception:
            return Response({
                "error": "Payment verification failed"
            }, status=400)
