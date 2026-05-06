from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
import random
from django.core.mail import send_mail
from django.conf import settings

from .models import UserToken, PasswordResetOTP
from .serializers import (
    RegisterSerializer,
    UserSerializer,
    VerifyOTPSerializer,
    ResetPasswordSerializer
)

User = get_user_model()


# 🔹 REGISTER
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        user.is_active = False
        user.save()

        otp = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.create(user=user, otp=otp)

        send_mail(
            subject="V Perfume - OTP Verification",
            message=f"Your OTP is {otp}",
            from_email=f"V Perfume <{settings.EMAIL_HOST_USER}>",
            recipient_list=[user.email],
        )

        return Response({"message": "User registered. OTP sent"})


# 🔹 LOGIN
class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = str(request.data.get("password"))

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=401)

        if not user.is_active:
            return Response({"error": "Account not verified"}, status=403)

        refresh = RefreshToken.for_user(user)

        UserToken.objects.filter(user=user).delete()
        token_obj = UserToken(user=user)
        token_obj.set_token(str(refresh.access_token))
        token_obj.save()

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })


# 🔹 LOGOUT
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=400)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            UserToken.objects.filter(user=request.user).delete()

            return Response({"message": "Logged out"})
        except:
            return Response({"error": "Invalid token"}, status=400)


# 🔹 AUTH ME
class AuthMe(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


# 🔹 VERIFY OTP (REGISTER + FORGOT)
class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp = serializer.validated_data["otp"]

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        otp_obj = PasswordResetOTP.objects.filter(user=user).first()
        if not otp_obj:
            return Response({"error": "OTP not found"}, status=400)

        if otp_obj.is_expired():
            otp_obj.delete()
            return Response({"error": "OTP expired"}, status=400)

        if otp_obj.otp != otp:
            otp_obj.attempts += 1
            otp_obj.save()
            return Response({"error": "Invalid OTP"}, status=400)

        otp_obj.is_verified = True
        otp_obj.save()

        user.is_active = True
        user.save()

        return Response({"message": "OTP verified"})


# 🔹 FORGOT PASSWORD (SEND OTP)
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        PasswordResetOTP.objects.filter(user=user).delete()

        otp = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.create(user=user, otp=otp)

        send_mail(
            subject="V Perfume - Reset Password",
            message=f"Your OTP is {otp}",
            from_email=f"V Perfume <{settings.EMAIL_HOST_USER}>",
            recipient_list=[user.email],
        )

        return Response({"message": "OTP sent"})


# 🔹 RESET PASSWORD
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"error": "User not found"}, status=404)

        otp_obj = PasswordResetOTP.objects.filter(
            user=user,
            is_verified=True
        ).first()

        if not otp_obj:
            return Response({"error": "OTP not verified"}, status=400)

        user.set_password(password)
        user.save()

        otp_obj.delete()

        return Response({"message": "Password reset successful"})


# 🔹 CHANGE PASSWORD (LOGGED IN)
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        # 🔹 Check fields
        if not old_password or not new_password or not confirm_password:
            return Response({"error": "All fields are required"}, status=400)

        # 🔹 Check old password
        if not user.check_password(str(old_password)):
            return Response({"error": "Old password incorrect"}, status=400)

        # 🔹 Match new passwords
        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        # 🔹 Validate length
        if len(new_password) < 6:
            return Response({"error": "Password too short"}, status=400)

        # 🔹 Set new password
        user.set_password(str(new_password))
        user.save()

        return Response({"message": "Password changed successfully"})

# 🔹 PROFILE UPDATE
class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        name = request.data.get("name")
        email = request.data.get("email")

        # 🔹 Update name
        if name:
            user.name = name

        # 🔹 Update email (with check)
        if email:
            if User.objects.filter(email=email).exclude(id=user.id).exists():
                return Response({"error": "Email already exists"}, status=400)
            user.email = email

        user.save()

        return Response({
            "message": "Profile updated",
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        })
