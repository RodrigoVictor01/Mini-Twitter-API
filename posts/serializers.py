from rest_framework import serializers
from .models import Post
from drf_spectacular.utils import extend_schema_field



class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['likes']

class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()
    
    
    likes = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    liked_by = serializers.SerializerMethodField()
    
    
    
    def create(self, validated_data):
        post = Post.objects.create(**validated_data)
        return post
    
    @extend_schema_field(serializers.IntegerField())
    def get_likes(self, obj):
        return obj.likes.count()
    
    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_liked_by(self, obj):
        return [user.username for user in obj.likes.all()]
    
    @extend_schema_field(serializers.CharField())
    def get_author(self, obj):
        if obj and obj.author:
            return obj.author.username
        
    
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'likes', 'liked_by']
        read_only_fields = ['id','author', 'likes', 'created_at', 'liked_by']
