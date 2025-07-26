from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema

from blog.models import Post
from users.models import Profile
from blog.serializers import PostSerializer
from users.serializers import ProfileSerializer, RegisterSerializer, LoginSerializer, UserSerializer, LogoutSerializer
from api.permissions import IsAdminOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]
    
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]
    

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=RegisterSerializer,
        responses={
            201: {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'username': {'type': 'string'},
                            'email': {'type': 'string'},
                            'first_name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                        }
                    },
                    'token': {'type': 'string'},
                    'access': {'type': 'string'},
                }
            }
        }
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=LoginSerializer,
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'user': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer'},
                            'username': {'type': 'string'},
                            'email': {'type': 'string'},
                            'first_name': {'type': 'string'},
                            'last_name': {'type': 'string'},
                        }
                    },
                    'refresh': {'type': 'string'},
                    'access': {'type': 'string'},
                }
            }
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'username': {'type': 'string'},
                    'email': {'type': 'string'},
                    'first_name': {'type': 'string'},
                    'last_name': {'type': 'string'},
                    'date_joined': {'type': 'string', 'format': 'date-time'},
                }
            }
        }
    )
    def get(self, request):
        return Response(UserSerializer(request.user).data)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=LogoutSerializer,
        responses={
            205: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)