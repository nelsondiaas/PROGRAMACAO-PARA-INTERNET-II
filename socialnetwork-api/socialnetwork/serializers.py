from django.contrib.auth import get_user_model
from rest_framework import serializers
from socialnetwork.models import *

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['pk', 'username', 'email']


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'suite', 'city', 'zipcode']


class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    
    class Meta:
        model = Profile
        fields = ['pk', 'name', 'email', 'address']
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('address')
        address = instance.address
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)
        address.street = address_data.get('street', address.street)
        address.suite = address_data.get('city', address.suite)
        address.zipcode = address_data.get('zipcode', address.zipcode)
        instance.save()
        address.save()
        return instance


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'userId', 'title', 'body']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        instance.save()
        return instance


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['postId', 'name', 'email', 'body']


class ProfileListPostSerializer(serializers.ModelSerializer):
    posts = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="post-comments-detail")
    url = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="profile-post-detail")

    class Meta:
        model = Profile
        fields = ['url', 'name', 'email', 'posts']


class PostListCommentSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="post-comments-detail")
    comments = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name='comment-detail')
    
    class Meta:
        model = Post
        fields = ['url', 'title', 'body', 'comments']


class CommentDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(many=False, read_only=True, view_name="comment-detail")

    class Meta:
        model = Comment
        fields = ['url', 'name', 'email', 'body']


