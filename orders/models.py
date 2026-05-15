from django.db import models
from django.contrib.auth import get_user_model
from products.models import Perfume

User = get_user_model()


class Order(models.Model):

    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("PLACED", "Placed"),
        ("SHIPPED", "Shipped"),
        ("DELIVERED", "Delivered"),
        ("CANCELLED", "Cancelled"),
    )

    PAYMENT_CHOICES = (
        ("COD", "Cash on Delivery"),
        ("ONLINE", "Online"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    is_paid = models.BooleanField(default=False)
    razorpay_order_id = models.CharField(max_length=255,blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=255,blank=True, null=True)
    is_buy_now = models.BooleanField(default=False)


    


    def __str__(self):
        return f"Order {self.id} - {self.user.email}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.perfume.name
