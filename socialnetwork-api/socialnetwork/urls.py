from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('api-token/', CustomAuthToken.as_view(), name='api-token'),
    
    path('api/v1/users/', UserList.as_view(), name='users-list'),

    path('api/v1/profiles/', ProfileList.as_view(), name='profiles-list'),
    path('api/v1/profiles/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),
    
    path('api/v1/profiles-posts/', ProfilePostList.as_view(), name='profiles-posts-list'),
    path('api/v1/profiles-posts/<int:pk>/', ProfilePostDetail.as_view(), name='profile-post-detail'),
    
    path('api/v1/posts-comments/', PostCommentList.as_view(), name='posts-comments-list'),
    path('api/v1/posts-comments/<int:pk>/', PostDetailWithCommentList.as_view(), name='post-comments-detail'),
    
    path('api/v1/posts/<int:pk>/comments/', CommentView.as_view(), name='comments-list'),
    path('api/v1/posts/comments/<int:pk>/', CommentDetail.as_view(), name='comment-detail'),

    path('api/v1/profiles-detail/', AmountPostAndCommentFromProfile.as_view(), name='profiles-detail-posts-comments'),
    path('', ApiRoot.as_view())
    
]


