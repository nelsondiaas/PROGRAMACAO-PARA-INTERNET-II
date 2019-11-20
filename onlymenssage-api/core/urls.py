from django.urls import path, include
from .views import *


urlpatterns = [

    path('api-token/', MyTokenObtainPairView.as_view(), name='api-token'),

    path('api/v1/profiles/', ProfileListView.as_view(), name='profile-list-view'),

    path('api/v1/profiles/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail-view'),

]