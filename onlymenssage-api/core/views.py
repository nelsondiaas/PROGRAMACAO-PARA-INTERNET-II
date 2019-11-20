from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .paginator import Paginator
from django.http import Http404
from .permissions import *
from .serializers import *
from .models import *

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ProfileListView(Paginator, APIView):

    permission_classes = [ReadOnly]
    pagination_class = PageNumberPagination
    
    def get(self, request, format=None):
        profiles = Profile.objects.get_queryset().order_by('id')
        page = self.paginate_queryset(profiles)
        profile_serializer = ProfileListViewSerializer(profiles, many=True)
        return self.get_paginated_response(profile_serializer.data)

    def post(self, request, format=None):
        profile_serializer = ProfileSerializer(data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    