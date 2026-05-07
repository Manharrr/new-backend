from django.urls import path
from .views import ( RegisterView,LoginView,LogoutView,AuthMe,VerifyOTPView,ForgotPasswordView,ResetPasswordView,ChangePasswordView,ProfileUpdateView,
)

urlpatterns = [
    #  Auth
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),

    #  User
    path('me/', AuthMe.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),

    #  OTP / Verification
    path('verify-otp/', VerifyOTPView.as_view()),

    #  Forgot Password
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('reset-password/', ResetPasswordView.as_view()),

    #  Change Password 
    path('change-password/', ChangePasswordView.as_view()),
]

#resent otp cheyyanam