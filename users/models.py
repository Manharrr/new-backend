from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    def create_user(self,email,password=None,**extra_fields):
        if not email:
            raise ValueError("Email required")
        
        user=self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password):
        user=self.create_user(email,password)
        user.is_staff =True
        user.is_superuser =True
        user.save()
        return user
    
class User(AbstractBaseUser,PermissionsMixin):
    name=models.CharField(max_length=40)
    email=models.EmailField(unique=True)
    is_active=models.BooleanField(default=True)
    is_staff=models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True) 
    role = models.CharField(max_length=10,choices=[("admin", "Admin"), ("customer", "Customer")],default="customer")
    attempts = models.IntegerField(default=0)      


    objects=UserManager()

    USERNAME_FIELD = "email"
    def __str__(self):
        return self.name


# 🔹 Access Token Storage (for logout control)
class UserToken(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    access_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    
class PasswordResetOTP(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    otp = models.CharField( max_length=6)
    attempts = models.IntegerField(default=0)   
    created_at=models.DateTimeField(auto_now_add=True)
    is_verified=models.BooleanField(default=False)