from django.urls import path
from .views import *

urlpatterns = [

    path('api/v1/profiles/', ProfileCreateOrList.as_view()),
    path('api/v1/profiles/<int:pk>/', ProfileDetail.as_view()),
    path('api/v1/profiles-posts/', ProfilePost.as_view()),
    path('api/v1/profiles/<int:pk>/posts/', ProfilePost.as_view()),
    path('api/v1/profiles-posts/<int:pk>/', ProfilePostDetail.as_view()),
    path('api/v1/posts-comments/', PostListWithComment.as_view()),
    path('api/v1/posts-comments/<int:pk>/', PostListWithCommentDetail.as_view()),
    path('api/v1/posts/<int:pk>/comments/', CommentCreateOrList.as_view()),
    path('api/v1/posts/<int:pk_post>/comments/<int:pk_comment>/', CommentDetail.as_view()),
    path('api/v1/profiles-detail/', AmountPostAndCommentFromProfile.as_view())
    
]


