from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status
from django.http import Http404
from .serializers import *
from .permissions import *
from .models import *

User = get_user_model()

class ApiRoot(APIView):

    def get(self, request, *args, **kwargs):

        data = {

            'users': reverse('users-list', request=request),
            'profiles': reverse('profiles-list', request=request),
            'profiles-posts': reverse('posts-list', request=request),
            'posts-comments': reverse('comments-list', request=request),
            'profiles-detail': reverse('profiles-detail-posts-comments', request=request),
        }

        return Response(data, status=status.HTTP_200_OK)

class UserList(APIView):

    permission_classes = [IsUserOrReadOnly]

    def get(self, request, format=None):
        user = User.objects.all()
        self.check_object_permissions(request, User)
        user_serializer = UserSerializer(user, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)

class ProfileList(APIView):

    permission_classes = [IsProfileOrReadOnly]

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        self.check_object_permissions(request, Profile)
        profile_serializer = ProfileSerializer(profiles, many=True)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)

class ProfileDetail(APIView):

    permission_classes = [IsProfileOrReadOnly]

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
        return Response(status=status.HTTP_200_OK)

class PostList(APIView):

    permission_classes = [PostIsOwnerOrReadOnly]

    def get(self, request, format=None):
        profiles = Profile.objects.all()
        profile_serializer = ProfileListPostSerializer(profiles, many=True)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    
class PostDetail(APIView):

    permission_classes = [PostIsOwnerOrReadOnly]

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        profile_serializer = ProfileListPostSerializer(profile, many=False)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        self.get_object(Profile, pk)
        request.data['userId'] = pk
        profile_serializer = PostSerializer(data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_201_CREATED)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        post = self.get_object(Post, pk)
        self.check_object_permissions(request, post)
        request.data['userId'] = post.userId_id
        request.data['pk'] = pk
        profile_serializer = PostSerializer(post, data=request.data)
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(Post, pk)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_200_OK)

class CommentList(APIView):

    permission_classes = [CommentIsOwnerOrReadOnly]

    def get(self, request, format=None):
        post = Post.objects.all()
        post_serializer = PostListCommentSerializer(post, many=True)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

class PostListWithCommentDetail(APIView):

    permission_classes = [CommentIsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        post_serializer = PostListCommentSerializer(post, many=False)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

class CommentCreateOrList(APIView):

    permission_classes = [CommentIsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            return Comment.objects.filter(postId=pk)
        except Comment.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        comment = self.get_object(pk)
        comment_serializer = CommentSerializer(comment, many=True)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        request.data['postId'] = pk
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentDetail(APIView):

    permission_classes = [CommentIsOwnerOrReadOnly]

    def get_comment(self, pk_post, pk_comment):
        try:
            post = Comment.objects.filter(postId=pk_post)
            try:
                return post.get(pk=pk_comment)
            except Comment.DoesNotExist:
                raise Http404
        except Post.DoesNotExist:
            raise Http404
        
    def get(self, request, pk_post, pk_comment, format=None):
        comment = self.get_comment(pk_post, pk_comment)
        comment_serializer = CommentSerializer(comment, many=False)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk_post, pk_comment, format=None):
        comment = self.get_comment(pk_post, pk_comment)
        request.data['postId'] = pk_post
        comment_serializer = CommentSerializer(comment, data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk_post, pk_comment, format=None):
        comment = self.get_comment(pk_post, pk_comment)
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_200_OK)

class AmountPostAndCommentFromProfile(APIView):

    def get(self, request, format=None):
        profiles = Profile.objects.all()
       
        profiles_detail = []
        
        for profile in profiles:
            info = {}
            amount_post = Post.objects.filter(userId=profile.pk)
            info['pk'] = profile.pk
            info['name'] = profile.name
            info['amount_posts'] = len(amount_post)
            info['amount_comments'] = 0
            for post in amount_post:
                amount_comment = Comment.objects.filter(postId=post.pk)
                info['amount_comments'] += len(amount_comment)
            profiles_detail.append(info)
        
        return Response(profiles_detail, status=status.HTTP_200_OK)

class CustomAuthToken(ObtainAuthToken):

    throttle_scope = 'api-token'
    throttle_classes = [ScopedRateThrottle]
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        self.check_throttles(request) 
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk, 
            'name': user.username, 
            'email': user.email},
            status=status.HTTP_200_OK)

