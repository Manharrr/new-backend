from django.shortcuts import render
from rest_framework .views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt .tokens import RefreshToken
from .models import UserToken
from .serializers import RegisterSerializer,UserSerializer,sendOTpSerilaizer,ResetPasswordSerializer
from .models import PasswordResetOTP
import random
from django.core.mail import send_mail
from .permissions import IsAdmin



User=get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            # 🔥 generate OTP
            otp = str(random.randint(100000, 999999))

            PasswordResetOTP.objects.create(
                user=user,
                otp=otp
            )

            # 🔥 send email
            send_mail(
                "Verify your account",
                f"Your OTP is {otp}",
                "yourgmail@gmail.com",
                [user.email],
            )

            return Response({"message": "User registered. OTP sent."}, status=201)

        return Response(serializer.errors, status=400)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            access = str(refresh.access_token)

            # 🔥 store access token
            UserToken.objects.create(
                user=user,
                access_token=access
            )

            return Response({
                "access": access,
                "refresh": str(refresh),
            })

        return Response({"error": "Invalid credentials"}, status=401)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)

            # blacklist refresh token
            token.blacklist()

            # 🔥 delete access token
            auth = request.headers.get("Authorization")
            if not auth or " " not in auth:
                return Response({"error": "No token"}, status=400)

            access = auth.split(" ")[1]
            UserToken.objects.filter(access_token=access).delete()

            return Response({"message": "Logged out"})
        except:
            return Response({"error": "Invalid token"}, status=400)

class AuthMe(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,request):
        serializer=UserSerializer(request.user)
        return Response(serializer.data)
    

class SentotpView(APIView):
    def post(self,request):
        serializer=sendOTpSerilaizer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email=serializer.validated_data['email']
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error":"Email not register"},status=400)
        
        otp = str(random.randint(100000, 999999))
        PasswordResetOTP.objects.filter(user=user).delete()

        PasswordResetOTP.objects.create(
            user=user,
            otp=otp
        )

        send_mail(
            "Password Reset OTP",
            f"Your OTP is {otp}. Valid for 5 minutes.",
            "noreply@example.com",
            [email],
        )

        return Response({"message": "OTP sent successfully"}, status=200)
    

from datetime import timedelta
from django.utils import timezone

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_obj =PasswordResetOTP.objects.get(user=user, otp=otp)
        except:
            return Response({"error": "Invalid OTP"}, status=400)

        if timezone.now() > otp_obj.created_at + timedelta(minutes=5):
            otp_obj.delete()
            return Response({"error": "OTP expired"}, status=400)

        otp_obj.is_verified = True
        otp_obj.save()

        return Response({"message": "OTP verified"})
    

class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("password")

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.get(user=user, is_verified=True)
        except:
            return Response({"error": "OTP not verified"}, status=400)

        user.set_password(new_password)
        user.save()

        otp_obj.delete()

        return Response({"message": "Password reset successful"})
    

class ProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        name = request.data.get("name")
        if name:
            user.name = name

        user.save()

        return Response({"message": "Profile updated"})
    
class VerifyAccountView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_obj = PasswordResetOTP.objects.get(user=user)
        except User.DoesNotExist:
            return Response({"error": "Invalid email"}, status=400)
        except PasswordResetOTP.DoesNotExist:
            return Response({"error": "No OTP found"}, status=400)

        # 🔥 ADD THIS HERE (attempt check)
        if otp_obj.attempts >= 3:
            return Response({"error": "Too many attempts"}, status=400)

        # 🔥 ADD THIS HERE (wrong OTP)
        if otp_obj.otp != otp:
            otp_obj.attempts += 1
            otp_obj.save()
            return Response({"error": "Invalid OTP"}, status=400)

        # ✅ success
        otp_obj.is_verified = True
        otp_obj.save()

        user.is_active = True
        user.save()

        return Response({"message": "Account verified"})

