from rest_framework.routers import DefaultRouter
from .views import PostViewSet, ProfileViewSet
from .views import RegisterUserView, MeView
from django.urls import path


router = DefaultRouter()

router.register(r'blogs', PostViewSet, basename='post')
router.register(r'users', ProfileViewSet, basename='profile')

urlpatterns = [
    path('users/register/', RegisterUserView.as_view(), name='user-register'),
    path('users/me/', MeView.as_view(), name='user-me'),
]