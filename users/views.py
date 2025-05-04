from .models import User
from rest_framework import generics
from .serializers import UserSignupSerializer, UserSerializer, UserLoginSerializer
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Authentication'])
class UserSignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer

@extend_schema(tags=['Authentication'])
class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'detail': 'Email and password are required'}, status=500)

        user = User.objects.filter(email=email).first()
    
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                },
                'message': 'Login successful',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })

        return Response({'detail': 'Invalid credentials'}, status=401)

@extend_schema(tags=['Users'])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.all()

    @action(detail=True, methods=['post'])
    def follow(self, request, pk=None):
        user_to_follow = self.get_object()
        if user_to_follow == request.user:
            return Response({'detail': "You can't follow yourself"}, status=400)
        
        if user_to_follow in request.user.following.all():
            return Response({'detail': f'You are already following {user_to_follow.username}'}, status=400)
        
        request.user.following.add(user_to_follow)
        return Response({'detail': f'You are now following {user_to_follow.username}'})

    @action(detail=True, methods=['post'])
    def unfollow(self, request, pk=None):
        user_to_unfollow = self.get_object()
        if user_to_unfollow == request.user:
            return Response({'detail': "You can't unfollow yourself"}, status=400)
        
        request.user.following.remove(user_to_unfollow)
        return Response({'detail': f'You have unfollowed {user_to_unfollow.username}'})

    @action(detail=True, methods=['get'])
    def followers(self, request, pk=None):
        user = self.get_object()
        followers = user.followers.all()
        serializer = UserSerializer(followers, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def following(self, request, pk=None):
        user = self.get_object()
        following = user.following.all()
        serializer = UserSerializer(following, many=True)
        return Response(serializer.data)




