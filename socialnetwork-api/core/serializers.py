from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import *

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
    
    def create(self, validated_data):
        name = validated_data['name'].split(" ")[0]
        email = validated_data['email']
        password = 'admin@123'
        request_address = validated_data.pop('address')
        new_user = User.objects.create_user(username=name, email=email, password=password)
        new_user.save()
        address = Address.objects.create(**request_address)
        return Profile.objects.create(user=new_user, address=address, **validated_data)
    
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
        fields = ['pk', 'postId', 'name', 'email', 'body']

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

