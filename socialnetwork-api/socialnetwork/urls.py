from django.conf.urls import url
from .views import *

urlpatterns = [

   
    url('api/v1/profiles/', ProfileCreateOrList.as_view()),
    url('api/v1/profiles/<int:pk>/', ProfileDetail.as_view()),
    url('api/v1/profiles-posts/', ProfilePost.as_view()),
    url('api/v1/profiles-posts/<int:pk>/', ProfilePostDetail.as_view()),
    url('api/v1/posts-comments/', PostListWithComment.as_view()),
    url('api/v1/posts-comments/<int:pk>/', PostListWithCommentDetail.as_view()),
    url('api/v1/posts/<int:pk>/comments/', CommentCreateOrList.as_view()),
    url('api/v1/posts/<int:pk_post>/comments/<int:pk_comment>/', CommentDetail.as_view()),
    url('api/v1/profiles-detail/', AmountPostAndCommentFromProfile.as_view()),
    url('', Root.as_view()),
    
]


