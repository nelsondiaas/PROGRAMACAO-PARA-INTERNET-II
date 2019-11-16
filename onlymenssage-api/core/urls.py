from django.urls import path
from .views import *

urlpatterns = [

    path('api/v1/profiles/', ProfileList.as_view(), name='profile-list'),

]