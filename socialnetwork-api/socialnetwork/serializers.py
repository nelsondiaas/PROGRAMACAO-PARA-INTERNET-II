from rest_framework import serializers
from socialnetwork.models import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['userId', 'title', 'body']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['postId', 'name', 'email', 'body']

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
        request_address = validated_data.pop('address')
        address = Address.objects.create(**request_address)
        return Profile.objects.create(address=address ,**validated_data)
     
        



