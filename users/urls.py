from django.urls import path
from .views import RegisterView,LoginView,LogoutView,AuthMe,ResetPasswordView,VerifyOTPView,SentotpView,VerifyAccountView,ProfileUpdateView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('logout/',LogoutView.as_view()),
    path('auth/me/',AuthMe.as_view()),
    path('forget-password/',SentotpView.as_view()),
    path('verify-otp/',VerifyOTPView.as_view()),
    path('reset-password/',ResetPasswordView.as_view()),
    path('verify-account/', VerifyAccountView.as_view()),
    path('profile/update/', ProfileUpdateView.as_view()),
    

]
