from django.urls import path
from users.views import UserViewSet, UserSignupView, LoginAPIView

urlpatterns = [
    path('signup/', UserSignupView.as_view(), name='user-signup'),
    path('login/', LoginAPIView.as_view(), name='login'),

    path('list/', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('detail/<int:pk>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),

    path('follow/<int:pk>/', UserViewSet.as_view({'post': 'follow'}), name='user-follow'),
    path('unfollow/<int:pk>/', UserViewSet.as_view({'post': 'unfollow'}), name='user-unfollow'),
    path('followers/<int:pk>/', UserViewSet.as_view({'get': 'followers'}), name='user-followers'),
    path('following/<int:pk>/', UserViewSet.as_view({'get': 'following'}), name='user-following'),
]
