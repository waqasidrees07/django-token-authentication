from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', SignInView.as_view()),
    path('me', UserAPIView.as_view()),
    path('update-user', UserPatchAPIView.as_view(), name='update-user'),
    path('forgot-password/', ForgotPassword.as_view()),
    path('reset-password/', ResetPassword.as_view()),
    path('update-password/', PasswordUpdateView.as_view(), name='password-update'),
]