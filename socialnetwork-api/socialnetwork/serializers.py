from django.contrib.auth import get_user_model
from rest_framework import serializers
from socialnetwork.models import *

User = get_user_model()

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
        name = validated_data['name'].split(" ")[0]
        email = validated_data['email']
        password = 'admin@123'
        request_address = validated_data.pop('address')
        new_user = User.objects.create_user(username=name, email=email, password=password)
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
        fields = ['userId', 'title', 'body']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'postId', 'name', 'email', 'body']

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

