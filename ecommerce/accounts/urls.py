from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import (
    RegisterView, MyTokenObtainPairView, ProfileView,
    LogoutView, AddressViewSet,
)

router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', MyTokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
] + router.urls