from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


# 🔹 REGISTER
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password too short")
        return value


# 🔹 USER RESPONSE
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email','is_staff')


# 🔹 VERIFY OTP
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        if not User.objects.filter(email__iexact=data['email']).exists():
            raise serializers.ValidationError("User not found")

        if len(data['otp']) != 6:
            raise serializers.ValidationError("Invalid OTP")

        return data


# 🔹 RESET PASSWORD
class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)

    def validate_email(self, value):
        if not User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("User not found")
        return value

# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# import re

# User = get_user_model()


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ('name', 'email', 'password')

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)

#     def validate_email(self, value):
#         if User.objects.filter(email__iexact=value).exists():
#             raise serializers.ValidationError("Email already exists")
#         return value

#     def validate_password(self, value):
#         if len(value) < 6:
#             raise serializers.ValidationError("Password too short")
        
#         return value


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'name', 'email', 'role', 'is_staff')


# # class SendOTPSerializer(serializers.Serializer):
# #     email = serializers.EmailField()

# #     def validate_email(self, value):
# #         if not User.objects.filter(email__iexact=value).exists():
# #             raise serializers.ValidationError("User not found")
# #         return value


# class VerifyOTPSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     otp = serializers.CharField(max_length=6)


# class ResetPasswordSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(min_length=6)
# # from rest_framework import serializers
# # from django.contrib.auth import get_user_model

# # User = get_user_model()

# # class RegisterSerializer(serializers.ModelSerializer):
# #     password=serializers.CharField(write_only=True)

# #     class Meta:
# #         model=User
# #         fields=('name','email','password')

# #     def create(self, validated_data):
# #       return User.objects.create_user(
# #         email=validated_data['email'],
# #         password=validated_data['password'],
# #         name=validated_data['name']
# #     )
    
# #     def validate_email(self, value):
# #         if User.objects.filter(email__iexact=value).exists():
# #             raise serializers.ValidationError("Email already exists")
# #         return value
    
# #     def validate_password(self, value):
# #         if len(value) < 7:
# #             raise serializers.ValidationError("Password too short")
# #         return value

# # class UserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model=User
# #         fields = ('id', 'name', 'email', 'role', 'is_staff')



# # class sendOTpSerilaizer(serializers.Serializer):
# #     email=serializers.EmailField()

# #     def validate_email(self, value):
# #         if not User.objects.filter(email__iexact=value).exists():
# #             raise serializers.ValidationError("User not found")
# #         return value

# # class verifyOTPSerilaizer(serializers.Serializer):
# #     email=serializers.EmailField()
# #     otp=serializers.CharField(max_length=6)

# #     def validate(self, data):
# #         if not User.objects.filter(email__iexact=data['email']).exists():
# #             raise serializers.ValidationError("User not found")

# #         if len(data['otp']) != 6:
# #             raise serializers.ValidationError("Invalid OTP")

# #         return data

# # class ResetPasswordSerializer(serializers.Serializer):
# #     email = serializers.EmailField()
# #     password = serializers.CharField(min_length=6)

# #     def validate_email(self, value):
# #         if not User.objects.filter(email__iexact=value).exists():
# #             raise serializers.ValidationError("User not found")
# #         return value