from rest_framework import serializers
from socialnetwork.models import *

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'suite', 'city', 'zipcode']

class ProfileSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    
    class Meta:
        model = Profile
        fields = ['name', 'email', 'address']

    def create(self, validated_data):
        request_address = validated_data.pop('address')
        address = Address.objects.create(**request_address)
        return Profile.objects.create(address=address ,**validated_data)

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
        fields = ['userId', 'title', 'body']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['postId', 'name', 'email', 'body']

class ProfileListPostSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    
    class Meta:
        model = Profile
        fields = ['name', 'email', 'posts']

class PostListCommentSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = ['userId', 'title', 'body', 'comments']
