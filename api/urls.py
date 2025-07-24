from rest_framework.routers import DefaultRouter
from .views import PostViewSet, ProfileViewSet
from django.urls import path, include

router = DefaultRouter()

router.register(r'blogs', PostViewSet, basename='post')
router.register(r'users', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),   
]