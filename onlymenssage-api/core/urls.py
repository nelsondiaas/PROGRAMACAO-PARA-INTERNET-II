from django.urls import path, include
from .views import *


urlpatterns = [

    path('', ApiRoot.as_view()),

    path('api-token/', MyTokenObtainPairView.as_view(), name='api-token'),

    path('api/v1/profiles/', ProfileListView.as_view(), name='profile-list-view'),

    path('api/v1/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail-view'),

    path('api/v1/contacts/', ContactView.as_view(), name='contact-list-view'),

    path('api/v1/contacts/<int:pk>/', ContactDetailView.as_view(), name='contact-detail-view'),
    
    path('api/v1/profiles/<int:pk_sender>/contacts/<int:pk_target>/', ContactCreateView.as_view(), name='contact-create-view'),

    path('api/v1/contacts/<int:pk>/singlechats/', SingleChatView.as_view(), name='singlechat-view'),

    path('api/v1/contacts/singlechats/<int:pk>/', SingleChatList.as_view(), name='singlechat-list-view'),

    path('api/v1/singlechats/<int:pk>/messages/', MessageSingleChatView.as_view(), name='message-singlechat-view'),

    path('api/v1/singlechats/messages/<int:pk>/', MessageSingleChatList.as_view(), name='message-singlechat-list-view'),

    path('api/v1/profiles/<int:pk>/singlechats/', ProfileSigleChatList.as_view(), name='profile-siglechat-list'),

    path('api/v1/profiles/<int:pk>/groupchats/', GroupChatView.as_view(), name='groupchat-view'),

    path('api/v1/profiles/groupchats/<int:pk>/', GroupChatList.as_view(), name='groupchat-list-view'),

    path('api/v1/profiles/<int:pk_profile>/groupchats/<int:pk_groupchat>/', GroupChatDetail.as_view(), name='groupchat-detail-view'),

    path('api/v1/groupchats/<int:pk>/groupmembers/', GroupMemberView.as_view(), name='groupmember-view'),

    path('api/v1/groupchats/groupmembers/<int:pk>/', GroupMemberList.as_view(), name='groupmember-list-view'),

    path('api/v1/groupchats/<int:pk>/messages/', MessageGroupChatView.as_view(), name='message-groupchat-view'),

    path('api/v1/groupchats/messages/<int:pk>/', MessageGroupChatList.as_view(), name='message-groupchat-list-view'),
    
    path('api/v1/groupmember/<int:pk>/admin/', GroupMemberAdminView.as_view(), name='groupmember-admin-view'),
    
]
