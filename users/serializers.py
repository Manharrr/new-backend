from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)

    class Meta:
        model=User
        fields=('name','email','password')

    def create(self,validated_data):
        return User.objects.create_user(**validated_data)
    
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value
    
    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError("Password too short")
        return value

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','email','is_staff')



class sendOTpSerilaizer(serializers.Serializer):
    email=serializers.EmailField()

class verifyOTPSerilaizer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=6)

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=6)