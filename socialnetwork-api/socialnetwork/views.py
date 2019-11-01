from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *
from .models import *
import json

class FileLoad(APIView):

    def post(self, request, format=None):
        profiles = request.data['users']
        posts = request.data['posts']
        comments = request.data['comments']

        for profile in profiles:
            address = profile['address']
            address_serializer = AddressSerializer(data=address)
            if address_serializer.is_valid():
                address_serializer.save()

            new_profile = profile
            new_profile['address'] = profile['id']
            profile_serializer = ProfileSerializer(data=new_profile)
            if profile_serializer.is_valid():
                profile_serializer.save()

        for post in posts:
            post_serializer = PostSerializer(data=post)
            if post_serializer.is_valid():
                post_serializer.save()

        for comment in comments:
            comment_serializer = CommentSerializer(data=comment)
            if comment_serializer.is_valid():
                comment_serializer.save()
        
        return Response(status=status.HTTP_201_CREATED)

class ProfileCreateOrList(APIView):

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        profile_serializer = ProfileSerializer(profiles, many=True)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        profile_serializer = ProfileSerializer(data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileDetail(APIView):

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile_serializer = ProfileSerializer(profile)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile_serializer = ProfileSerializer(profile, data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        profile = self.get_object(pk)
        profile.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProfilePost(APIView):

    def get(self, request, format=None):
        post = Post.objects.all()
        post_serializer = PostSerializer(post, many=True)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

class ProfilePostDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
            
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        post_serializer = PostSerializer(post)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

class CommentCreateOrList(APIView):

    def get_object(self, pk):
        try:
            return Comment.objects.filter(postId=pk)
        except Comment.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        comment_serializer = CommentSerializer(comment, many=True)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

class CommentDetail(APIView):

    def get_comment(self, pk_post, pk_comment):
        try:
            comments = Comment.objects.filter(postId=pk_post)
            return comments.get(pk=pk_comment)
        except Comment.DoesNotExist:
            raise Http404
    
    def get_post(self, post_id):
        try:
            return Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk_post, pk_comment, format=None):
        comment = self.get_comment(pk_post, pk_comment)
        comment_serializer = CommentSerializer(comment)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    '''
    def post(self, request, format=None):
        post = self.get_post(request.data['postId'])
        print("\nTESTS: ", )
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            post_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    '''
