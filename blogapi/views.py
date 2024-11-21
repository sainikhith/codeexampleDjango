from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from blog.models import Post
from .serializers import PostSerializer

from rest_framework.permissions import IsAuthenticated

from rest_framework_api_key.permissions import HasAPIKey

from drf_yasg.utils import swagger_auto_schema


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
# @permission_classes([HasAPIKey])
def getAllPosts(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response({
        "status": True,
        "data": serializer.data
        })

@api_view(['GET'])
def getPostById(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)
    
    serializer = PostSerializer(post)
    return Response(serializer.data)

@swagger_auto_schema(method='post',request_body=PostSerializer)
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def addPosts(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)  # Return 201 Created status
    return Response(serializer.errors, status=400)

@api_view(['PUT'])
def updatePost(request, id):
    try:
        post = Post.objects.get(id=id)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)

@api_view(['DELETE'])
def deletePost(request, id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response({"error": "Post not found"}, status=404)
    
    post.delete()
    return Response({"message": "Post deleted successfully"})