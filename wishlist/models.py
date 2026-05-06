from django.db import models
from django.contrib.auth import get_user_model
from products.models import Perfume

User = get_user_model()

class Wishlist(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}"
    
class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['wishlist', 'perfume']  

    def __str__(self):
        return self.perfume.name

