from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import PostSerializer
from blog.models import Post
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': 'api/blogs'},
        {'GET': 'api/blog/id'},
    ]
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getBlogs(request):
    blogs = Post.objects.all()
    serializer = PostSerializer(blogs, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getBlog(request, pk):
    blog = Post.objects.get(id=pk)
    serializer = PostSerializer(blog, many=False)
    return Response(serializer.data)