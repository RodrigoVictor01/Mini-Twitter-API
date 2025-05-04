from rest_framework import serializers
from .models import User
from drf_spectacular.utils import extend_schema_field

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']



class UserSerializer(serializers.ModelSerializer):
    followers = serializers.SerializerMethodField()
    following = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()


    @extend_schema_field(UserSimpleSerializer(many=True))
    def get_followers(self, obj):
        followers = obj.followers.all()
        return UserSimpleSerializer(followers, many=True).data

    @extend_schema_field(UserSimpleSerializer(many=True))
    def get_following(self, obj):
        following = obj.following.all()
        return UserSimpleSerializer(following, many=True).data
    
    @extend_schema_field(serializers.IntegerField())
    def get_followers_count(self, obj):
        return obj.followers.count()
    
    @extend_schema_field(serializers.IntegerField())
    def get_following_count(self, obj):
        return obj.following.count()
        
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'followers', 'following',
                  'followers_count', 'following_count']




class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
