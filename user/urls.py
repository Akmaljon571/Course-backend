from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('register/code/', RegisterCodeView.as_view()),
    path('register/create/', RegisterCreateView.as_view()),
    path('parol/', PasswordEmailView.as_view()),
    path('parol/code/', PasswordCodeView.as_view()),
    path('login/', LoginView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('profile/', UserProfileDetail.as_view()),
]
