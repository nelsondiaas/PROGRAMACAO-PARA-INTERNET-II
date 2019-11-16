from django.contrib.auth import get_user_model
from rest_framework import serializers
from core.models import *

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(source='user.password')
    email = serializers.CharField(source='user.email')

    class Meta:
        model = Profile
        fields = ['pk', 'username', 'password', 'email', 'status']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data['user'])
        user.save()
        return Profile.objects.create(user=user, status=validated_data['status'])

class ProfileDetail(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.CharField(source='user.email')
    
    class Meta:
        model = Profile
        fields = ['pk', 'username', 'email', 'status']