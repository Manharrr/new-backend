# payments/serializers.py

from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Payment

        fields = "__all__"


class CreatePaymentSerializer(serializers.Serializer):

    order_id = serializers.IntegerField()


class VerifyPaymentSerializer(serializers.Serializer):

    razorpay_order_id = serializers.CharField()

    razorpay_payment_id = serializers.CharField()

    razorpay_signature = serializers.CharField()