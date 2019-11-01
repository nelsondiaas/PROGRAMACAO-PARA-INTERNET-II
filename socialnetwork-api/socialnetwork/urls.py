from django.urls import path
from .views import *

urlpatterns = [

    path('api/v1/fileloads/', FileLoad.as_view()),
    path('api/v1/profiles/', ProfileCreateOrList.as_view()),
    path('api/v1/profiles/<int:pk>/', ProfileDetail.as_view()),
    path('api/v1/profiles-posts/', ProfilePost.as_view()),
    path('api/v1/profiles-posts/<int:pk>/', ProfilePostDetail.as_view())
    
]


