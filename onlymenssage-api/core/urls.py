from django.urls import path, include
from .views import *


urlpatterns = [

    path('', ApiRoot.as_view()),

    path('api-token/', MyTokenObtainPairView.as_view(), name='api-token'),

    path('api/v1/profiles/', ProfileListView.as_view(), name='profile-list-view'),

    path('api/v1/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail-view'),
    
    path('api/v1/profiles/<int:pk_sender>/contacts/<int:pk_target>/', ContactView.as_view(), name='contact-view'),
    
    path('api/v1/profiles-contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail'),

    path('api/v1/profiles/<int:pk_profile>/singlechat/<int:pk_contact>/', SingleChatView.as_view(), name='singlechat-view'),

    path('api/v1/profiles-singlechats/<int:pk>/', ProfileSingleChatList.as_view(), name='profile-singlechat-list'),

]
