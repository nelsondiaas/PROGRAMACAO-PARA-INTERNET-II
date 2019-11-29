from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView
from django.contrib.auth import get_user_model
from rest_framework import permissions
from .permissions import *
from .serializers import *

User = get_user_model()


class UserListView(ListAPIView):
    name = "user-list"
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClientListView(ListCreateAPIView):
    name = 'client-list-view'
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class ClientDetail(RetrieveUpdateDestroyAPIView):
    name = 'client-detail'
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class AddressListView(ListCreateAPIView):
    name = 'address-list-view'
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AddressDetail(RetrieveUpdateDestroyAPIView):
    name = 'address-detail'
    queryset = Address.objects.all()
    serializer_class = AddressSerializer


class AdministratorListView(ListCreateAPIView):
    name = 'administrator-list-view'
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer


class AdministratorDetail(RetrieveUpdateDestroyAPIView):
    name = 'administrator-detail'
    queryset = Administrator.objects.all()
    serializer_class = AdministratorSerializer


class ApiRoot(GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):

        data = {
            
            "address": reverse(AddressListView.name, request=request),
            "clients": reverse(ClientListView.name, request=request),
            "administrators": reverse(AdministratorListView.name, request=request),
        }
        
        return Response(data, status=status.HTTP_200_OK)