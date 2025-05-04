from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache
import redis
from django.core.cache.backends.base import InvalidCacheBackendError
from drf_spectacular.utils import extend_schema

from .models import Post
from .serializers import PostSerializer


@extend_schema(tags=['Posts'])
class PostCreateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@extend_schema(tags=['Posts'])
class PostListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    @extend_schema(operation_id="list_posts")
    def get(self, request):
        posts = Post.objects.all().order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)



@extend_schema(tags=['Posts'])
class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


@extend_schema(tags=['Posts'])
class PostUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def patch(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response({"error": "You can't edit this post"}, status=403)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

@extend_schema(tags=['Posts'])
class PostDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        if post.author != request.user:
            return Response({"error": "You can't delete this post"}, status=403)
        post.delete()
        return Response(status=204)


@extend_schema(tags=['Posts'])
class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        
        if user in post.likes.all():
            post.likes.remove(user)
            return Response({"message": f"Like removed by {user}!"})
        else:
            post.likes.add(user)
            return Response({"message": f"Post liked by {user}!"})


@extend_schema(tags=['Feed'])
class FeedView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request):
        user = request.user
        page_number = request.query_params.get('page', '1')
        cache_key = f'feed_user_{user.id}_page_{page_number}'

        try:
            cached_data = cache.get(cache_key)
            if cached_data:
                return Response(cached_data)
        except (redis.exceptions.ConnectionError, InvalidCacheBackendError):
            return Response({'detail': 'Internal server error: Redis is not available'}, status=503)
        
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)

        following_users = user.following.all()
        posts = Post.objects.filter(author__in=following_users).order_by('-created_at')

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(posts, request)

        serializer = PostSerializer(result_page, many=True)
        response_data = paginator.get_paginated_response(serializer.data).data

        try:
            cache.set(cache_key, response_data, timeout=60)
        except (redis.exceptions.ConnectionError, InvalidCacheBackendError):
            pass

        return Response(response_data)

    