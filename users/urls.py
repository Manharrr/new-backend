from django.urls import path
from .views import ( RegisterView,LoginView,
                    LogoutView,AuthMe,VerifyOTPView,
                    ForgotPasswordView,ResetPasswordView,ChangePasswordView,
                    ProfileUpdateView,VerifyEmailView,GoogleLoginAPIView)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('logout/', LogoutView.as_view()),

    path('me/', AuthMe.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),

    path('verify-otp/', VerifyOTPView.as_view()),

    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),

    path('change-password/', ChangePasswordView.as_view()),
    path("verify-email/<str:token>/",VerifyEmailView.as_view()),

    path("google-login/", GoogleLoginAPIView.as_view()),
]

