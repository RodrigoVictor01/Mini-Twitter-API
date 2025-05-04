from django.urls import path
from .views import (
    PostCreateView,
    PostListView,
    PostUpdateView,
    PostDeleteView,
    PostLikeView,
    PostDetailView
)

urlpatterns = [
    path('create/', PostCreateView.as_view(), name='post-create'),
    path('list/', PostListView.as_view(), name='post-list'),
    path('list/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('edit/<int:pk>/', PostUpdateView.as_view(), name='post-edit'),
    path('delete/<int:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('like/<int:pk>/', PostLikeView.as_view(), name='post-like'),
]
