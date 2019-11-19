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
        fields = ['pk', 'name', 'email', 'address']

    def create(self, validated_data):
        name = validated_data['name'].split(" ")[0]
        email = validated_data['email']
        password = 'admin@123'
        request_address = validated_data.pop('address')
        new_user = User.objects.create_user(
        username=name, email=email, password=password)
        new_user.save()
        address = Address.objects.create(**request_address)
        return Profile.objects.create(user=new_user, address=address, **validated_data)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['pk', 'userId', 'title', 'body']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['pk', 'postId', 'name', 'email', 'body']

