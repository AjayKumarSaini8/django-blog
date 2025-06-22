from django.urls import path
from .views import (
    UserCreateView,
    CustomTokenObtainPairView,
    UserProfileView,
    UserRegistrationView
)

urlpatterns = [
    # API Endpoints
    path('api/register/', UserCreateView.as_view(), name='api-register'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='api-login'),
    path('api/profile/', UserProfileView.as_view(), name='api-profile'),
    
    # Frontend Endpoints
    path('register/', UserRegistrationView.as_view(), name='register'),
]