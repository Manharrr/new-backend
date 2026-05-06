from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


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

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)    

    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    perfume = models.ForeignKey(Perfume, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.IntegerField()
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.perfume}"