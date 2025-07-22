from rest_framework import viewsets
from blog.models import Post
from users.models import Profile
from blog.serializers import PostSerializer
from users.serializers import ProfileSerializer, RegisterSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from api.permissions import IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated, AllowAny

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class RegisterUserView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
class MeView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile