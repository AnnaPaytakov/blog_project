from rest_framework.routers import DefaultRouter
from .views import PostViewSet, ProfileViewSet, RegisterView, LoginView, LogoutView, ProfileView
from rest_framework_simplejwt.views import TokenRefreshView
from django.urls import path, include

router = DefaultRouter()

router.register(r'blogs', PostViewSet, basename='post')
router.register(r'users', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/profile/', ProfileView.as_view(), name='profile'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]