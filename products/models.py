from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class Category(models.Model):
    CATEGORY_CHOICES = (
        ("men", "Men"),
        ("women", "Women"),
        ("exclusive", "Exclusive"),
    )

    name = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name
class Perfume(models.Model):
    name = models.CharField(max_length=150)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)

    description = models.TextField()
    image = models.ImageField(upload_to='perfumes/', null=True, blank=True)

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class PerfumeVariant(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name='variants')
    
    size_ml = models.IntegerField()  # 50ml, 100ml
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()

    def __str__(self):
        return f"{self.perfume.name} - {self.size_ml}ml"
    

class Review(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField()  # 1–5
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.perfume.name}"