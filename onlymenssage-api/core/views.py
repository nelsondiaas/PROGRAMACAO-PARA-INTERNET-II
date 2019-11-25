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

    pagination_class = PageNumberPagination
    
    def get(self, request, format=None):
        profiles = Profile.objects.get_queryset().order_by('id')
        page = self.paginate_queryset(profiles)
        context = {'request': request}
        profile_serializer = ProfileListViewSerializer(profiles, context=context, many=True)
        return self.get_paginated_response(profile_serializer.data)

    def post(self, request, format=None):
        profile_serializer = ProfileSerializer(data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileDetailView(APIView):
    
    permission_classes = [IsAuthenticated, ProfileOwnerReadOnly]

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        context = {'request': request}
        profile_serializer = ProfileDetailViewSerializer(profile, context=context, many=False)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        self.check_object_permissions(request, profile)
        profile_serializer = ProfileDetailViewSerializer(profile, data=request.data, partial=True)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        self.check_object_permissions(request, profile)
        profile.delete()
        return Response(status=status.HTTP_200_OK)


class ContactView(APIView):

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def post(self, request, pk_sender, pk_target, format=None):
        sender = self.get_object(Profile, pk_sender)
        target = self.get_object(Profile, pk_target)
        request.data['profile'] = sender.pk;
        request.data['friend'] = target.pk;
        contact_serializer = ContactSerializer(data=request.data)
        if contact_serializer.is_valid():
            contact_serializer.save()
            return Response(contact_serializer.data, status=status.HTTP_201_CREATED)
        return Response(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ContactDetailView(Paginator, APIView):

    pagination_class = PageNumberPagination

    def get_object(self, obj, pk):
        try:
            profile = obj.objects.get(pk=pk)
            try:
                return Contact.objects.filter(profile=profile).all()
            except Contact.DoesNotExist:
                raise Http404
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        contacts = self.get_object(Profile, pk)
        page = self.paginate_queryset(contacts)
        context = {'request': request}
        contact_serializer = ContactDetailSerializer(contacts, context=context, many=True)
        return self.get_paginated_response(contact_serializer.data)


class SingleChatView(APIView):

    def get_object(self, obj, pk_profile, pk_contact):
        try:
            profile = obj.objects.get(pk=pk_profile)
            try:
                return Contact.objects.get(profile=profile, pk=pk_contact)
            except Contact.DoesNotExist:
                raise Http404
        except obj.DoesNotExist:
            raise Http404
    
    def post(self, request, pk_sender, pk_contact, format=None):
        contact = self.get_object(Profile, pk_sender, pk_contact)
        single_chat_serializer = SingleChatViewSerializer(contact, many=False)
        if single_chat_serializer.is_valid():
            single_chat_serializer.save()
            return Response(single_chat_serializer.data, status=status.HTTP_201_CREATED)
        return Response(single_chat_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApiRoot(APIView):

    def get(self, request, *args, **kwargs):

        data = {
            
            'profiles': reverse('profile-list-view', request=request),
  
        }

        return Response(data, status=status.HTTP_200_OK)
