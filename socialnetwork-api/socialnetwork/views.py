from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from rest_framework import status
from .paginator import Paginator
from django.http import Http404
from .serializers import *
from .permissions import *
from .models import *


User = get_user_model()


class ApiRoot(APIView):

    def get(self, request, *args, **kwargs):

        data = {
            
            'api-token': reverse('api-token', request=request),
            'users': reverse('users-list', request=request),
            'profiles': reverse('profiles-list', request=request),
            'profiles-posts': reverse('profiles-posts-list', request=request),
            'posts-comments': reverse('posts-comments-list', request=request),
            'profiles-detail': reverse('profiles-detail-posts-comments', request=request),
  
        }

        return Response(data, status=status.HTTP_200_OK)


class UserList(Paginator, APIView):

    permission_classes = [IsUserOrReadOnly]
    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        user = User.objects.get_queryset().order_by('id')
        self.check_object_permissions(request, User)
        page = self.paginate_queryset(user)
        user_serializer = UserSerializer(user, many=True)
        return self.get_paginated_response(user_serializer.data)


class ProfileList(Paginator, APIView):

    permission_classes = [IsProfileOrReadOnly]
    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        profiles = Profile.objects.get_queryset().order_by('id')
        self.check_object_permissions(request, Profile)
        page = self.paginate_queryset(profiles)
        profile_serializer = ProfileSerializer(profiles, many=True)
        return self.get_paginated_response(profile_serializer.data)


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


class ProfilePostList(Paginator, APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        profiles = Profile.objects.get_queryset().order_by('id')
        context = {'request': request}
        page = self.paginate_queryset(profiles)
        profile_serializer = ProfileListPostSerializer(profiles, context=context, many=True)
        return self.get_paginated_response(profile_serializer.data)


class PostCommentList(Paginator, APIView):

    pagination_class = PageNumberPagination

    def get(self, request, format=None):
        posts = Post.objects.get_queryset().order_by('id')
        context = {'request': request}
        page = self.paginate_queryset(posts)
        post_serializer = PostListCommentSerializer(posts, context=context, many=True)
        return self.get_paginated_response(post_serializer.data)


class PostDetailWithCommentList(APIView):

    permission_classes = [PostIsOwnerOrReadOnly]

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        post = self.get_object(Post, pk)
        context = {'request': request}
        post_serializer = PostListCommentSerializer(post, context=context, many=False)
        return Response(post_serializer.data, status=status.HTTP_200_OK)

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


class ProfilePostDetail(APIView):

    permission_classes = [IsProfileOrReadOnly]

    def get_object(self, obj, pk):
        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            raise Http404
        
    def get(self, request, pk, format=None):
        profile = self.get_object(Profile, pk)
        context = {'request': request}
        profile_serializer = ProfileListPostSerializer(profile, context=context, many=False)
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    

class CommentList(APIView):

    permission_classes = [CommentIsOwnerOrReadOnly]

    def get(self, request, format=None):
        post = Post.objects.all()
        context = {'request': request}
        post_serializer = PostListCommentSerializer(post, context=context, many=True)
        return Response(post_serializer.data, status=status.HTTP_200_OK)


class CommentView(APIView):

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        context = {'request': request}
        comment_serializer = CommentDetailSerializer(post.comments, context=context, many=True)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk, format=None):
        comment = request.data
        comment['postId'] = pk
        comment_serializer = CommentSerializer(data=comment)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):

    permission_classes = [CommentIsOwnerOrReadOnly]

    def get_comment(self, pk):
        try:
            return Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        comment = self.get_comment(pk)
        context = {'request': request}
        comment_serializer = CommentDetailSerializer(comment, context=context, many=False)
        return Response(comment_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, pk, format=None):
        request.data['postId'] = pk
        comment_serializer = CommentSerializer(data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_201_CREATED)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        comment = self.get_comment(pk)
        comment_serializer = CommentSerializer(comment, data=request.data)
        if comment_serializer.is_valid():
            comment_serializer.save()
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(comment_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        comment = self.get_comment(pk)
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

