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
        fields = ['url', 'is_superuser', 'username', 'email', 'is_staff']


class AddressSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Address
        fields = '__all__'


class ClientSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Client
        fields = ['url', 'name', 'email', 'phone', 'address']

    def create(self, validated_data):
        user_created = User.objects.create_user(
        username=validated_data['name'].split()[0],
        email=validated_data['email'], password='admin@123')
        return Client.objects.create(user=user_created, **validated_data)


class AdministratorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Administrator
        fields = ['url', 'name', 'email', 'cpf', 'salary']

    def create(self, validated_data):
        user_created = User.objects.create_user(
        username=validated_data['name'].split()[0],
        email=validated_data['email'], password='admin@123', is_staff=True)
        return Administrator.objects.create(user=user_created, **validated_data)


class EmployeeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Employee
        fields = ['url', 'name', 'email', 'cpf', 'salary', 'administrator']

    def create(self, validated_data):
        user_created = User.objects.create_user(
        username=validated_data['name'].split()[0],
        email=validated_data['email'], password='admin@123', is_staff=True)
        return Employee.objects.create(user=user_created, **validated_data)


class StatusSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Status
        fields = '__all__'


class StatusDetailSerializer(serializers.HyperlinkedModelSerializer):
    message = serializers.CharField(style={'input_type': 'charfild'})

    class Meta:
        model = Status
        fields = ['url', 'message']


class GenreSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Author
        fields = '__all__'


class WriteSerializer(serializers.HyperlinkedModelSerializer):

     class Meta:
        model = Write
        fields = '__all__'


class BookSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Book
        fields = '__all__'
    

class SaleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sale
        fields = ['url', 'client', 'employee', 'status', 'total', 'date_created']


class SaleDetailSerializer(serializers.HyperlinkedModelSerializer):
    total = serializers.FloatField(style={'input_type': 'interger'})

    class Meta:
        model = Sale
        fields = ['url', 'client', 'employee', 'status', 'total', 'date_created']


class ItemsaleSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Itemsale
        fields = ['url', 'book', 'amount', 'subtotal', 'sale']

    def create(self, validated_data):
        item_sale = Itemsale.objects.create(**validated_data)
        '''
        if item_sale.amount > item_sale.book.stock:
            raise serializers.ValidationError("Error: insufficient stock to perform this operation")
        '''
        item_sale.calc_amount
        item_sale.sub_stock
        item_sale.add_total_sale
        return item_sale

class AdministratorEmployeeList(serializers.HyperlinkedModelSerializer):
    employees = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="employee-detail")
    
    class Meta:
        model = Administrator
        fields = ['url', 'name', 'email', 'cpf', 'salary', 'employees']