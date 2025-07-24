from rest_framework import viewsets
from blog.models import Post
from users.models import Profile
from blog.serializers import PostSerializer
from users.serializers import ProfileSerializer
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAdminUser

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]