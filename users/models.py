from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from datetime import timedelta
import hashlib


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=40)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # role = models.CharField(
    #     max_length=10,
    #     choices=[("admin", "Admin"), ("customer", "Customer")],
    #     default="customer"
    # )

    # attempts = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email


class UserToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_token(self, raw_token):
        self.token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

    def check_token(self, raw_token):
        return self.token_hash == hashlib.sha256(raw_token.encode()).hexdigest()


class PasswordResetOTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)

    attempts = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    MAX_ATTEMPTS = 5

    def is_expired(self):
        return timezone.now() > self.expires_at

    def can_retry(self):
        return self.attempts < self.MAX_ATTEMPTS

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

# from django.db import models
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.utils import timezone
# from datetime import timedelta
# import hashlib

# class UserManager(BaseUserManager):

#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("Email is required")

#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)

#         if password:
#             user.set_password(password)
#         else:
#             user.set_unusable_password()

#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('role', 'admin')

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError("Superuser must have is_staff=True")
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError("Superuser must have is_superuser=True")

#         return self.create_user(email, password, **extra_fields)


# class User(AbstractBaseUser, PermissionsMixin):
#     ROLE_CHOICES = (
#         ("admin", "Admin"),
#         ("customer", "Customer"),
#     )

#     name = models.CharField(max_length=40)
#     email = models.EmailField(unique=True)

#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)

#     role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="customer")

#     attempts = models.IntegerField(default=0)  # login attempts (optional logic)

#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     objects = UserManager()

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ['name']

#     def __str__(self):
#         return self.email


# class UserToken(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     token_hash = models.CharField(max_length=64)  # SHA256 hash
#     created_at = models.DateTimeField(auto_now_add=True)

#     def set_token(self, raw_token):
#         self.token_hash = hashlib.sha256(raw_token.encode()).hexdigest()

#     def check_token(self, raw_token):
#         return self.token_hash == hashlib.sha256(raw_token.encode()).hexdigest()

#     def __str__(self):
#         return f"{self.user.email} token"


# class PasswordResetOTP(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     otp = models.CharField(max_length=6)

#     attempts = models.IntegerField(default=0)
#     is_verified = models.BooleanField(default=False)

#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField()

#     MAX_ATTEMPTS = 5

#     def is_expired(self):
#         return timezone.now() > self.expires_at

#     def can_retry(self):
#         return self.attempts < self.MAX_ATTEMPTS

#     def save(self, *args, **kwargs):
#         if not self.expires_at:
#             self.expires_at = timezone.now() + timedelta(minutes=10)
#         super().save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.user.email} - OTP"
    













# from django.db import models

# # Create your models here.
# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin,
# from django.utils import timezone
# from datetime import timedelta
# import hashlib

# class UserManager(BaseUserManager):
#     def create_user(self,email,password=None,**extra_fields):
#         if not email:
#             raise ValueError("Email required")
        
#         user=self.model(email=self.normalize_email(email),**extra_fields)
#         user.set_password(password)
#         user.save()
#         return user
    
#     def create_superuser(self, email, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True')

#         return self.create_user(email, password, **extra_fields)
    
# class User(AbstractBaseUser,PermissionsMixin):
#     name=models.CharField(max_length=40)
#     email=models.EmailField(unique=True)
#     is_active=models.BooleanField(default=True)
#     is_staff=models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True) 
#     updated_at = models.DateTimeField(auto_now=True) 
#     role = models.CharField(max_length=10,choices=[("admin", "Admin"), ("customer", "Customer")],default="customer")
#     attempts = models.IntegerField(default=0)      


#     objects=UserManager()

#     USERNAME_FIELD = "email"
#     def __str__(self):
#         return self.name


# # 🔹 Access Token Storage (for logout control)
# class UserToken(models.Model):
#     user = models.ForeignKey("users.User", on_delete=models.CASCADE)
#     access_token = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.email
    
# class PasswordResetOTP(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     otp = models.CharField( max_length=6)
#     attempts = models.IntegerField(default=0)   
#     created_at=models.DateTimeField(auto_now_add=True)
#     is_verified=models.BooleanField(default=False)