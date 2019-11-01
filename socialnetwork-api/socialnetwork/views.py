from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import *

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

            

