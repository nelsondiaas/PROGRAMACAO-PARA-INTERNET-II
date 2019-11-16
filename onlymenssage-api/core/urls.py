from django.urls import path, include
from .views import *


urlpatterns = [

    path('api-token/', MyTokenObtainPairView.as_view(), name='api-token'),

    path('api/v1/profiles/', ProfileList.as_view(), name='profile-list'),

    path('api/v1/hello-world/', HelloView.as_view(), name='hello-world'),
    
]