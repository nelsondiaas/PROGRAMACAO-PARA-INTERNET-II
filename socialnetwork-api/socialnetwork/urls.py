from django.urls import path, include
from .views import *

urlpatterns = [
    
    path('api-token/', CustomAuthToken.as_view(), name='api-token'),
    
    path('api/v1/users/', UserList.as_view(), name='users-list'),

    path('api/v1/profiles/', ProfileList.as_view(), name='profiles-list'),
    path('api/v1/profiles/<int:pk>/', ProfileDetail.as_view(), name='profile-detail'),

    path('api/v1/profiles-posts/', PostList.as_view(), name='posts-list'),
    path('api/v1/profiles-posts/<int:pk>/', PostDetail.as_view()),

    path('api/v1/posts-comments/', CommentList.as_view(), name='comments-list'),
    path('api/v1/posts-comments/<int:pk>/', PostListWithCommentDetail.as_view()),
    
    path('api/v1/posts/<int:pk>/comments/', CommentCreateOrList.as_view()),
    path('api/v1/posts/<int:pk_post>/comments/<int:pk_comment>/', CommentDetail.as_view()),

    path('api/v1/profiles-detail/', AmountPostAndCommentFromProfile.as_view(), name='profiles-detail-posts-comments'),
    path('', ApiRoot.as_view())
    
]


