from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart - {self.user}"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    variant = models.ForeignKey(
        PerfumeVariant,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['cart', 'variant']  # prevents duplicate items

    def __str__(self):
        return f"{self.variant} x {self.quantity}"

# from django.db import models
# from django.contrib.auth import get_user_model
# User = get_user_model()

# # Create your models here.

# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
#     variant = models.ForeignKey(PerfumeVariant, on_delete=models.CASCADE)

#     quantity = models.IntegerField(default=1)

#     def __str__(self):
#         return f"{self.variant} x {self.quantity}"