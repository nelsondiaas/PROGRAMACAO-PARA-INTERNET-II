from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import serializers
from rest_framework import status
from .models import *

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = User
        fields = ['url', 'username', 'email']


class AddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Client
        fields = ('url', 'name', 'email', 'phone', 'address')

    def create(self, validated_data):
        user_created = User.objects.create_user(
        username=validated_data['name'].split()[0],
        email=validated_data['email'], password='admin@123')
        return Client.objects.create(user=user_created, **validated_data)


class AdministratorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Administrator
        fields = ('url', 'name', 'email', 'cpf', 'salary')

    def create(self, validated_data):
        user_created = User.objects.create_user(
        username=validated_data['name'].split()[0],
        email=validated_data['email'], password='admin@123')
        return Administrator.objects.create(user=user_created, **validated_data)