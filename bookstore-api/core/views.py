from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.generics import *
from .permissions import *
from .serializers import *

User = get_user_model()


class UserListView(ListAPIView):
    name = "user-list"
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAdminUser]


class UserDetail(RetrieveUpdateDestroyAPIView):
    name = "user-detail"
    queryset = User.objects.get_queryset().order_by('id')
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAdminUser]


class ClientListView(ListCreateAPIView):
    name = 'client-list-view'
    queryset = Client.objects.get_queryset().order_by('id')
    serializer_class = ClientSerializer

    permission_classes = [permissions.IsAuthenticated, ClientPermissions]


class ClientDetail(RetrieveUpdateDestroyAPIView):
    name = 'client-detail'
    queryset = Client.objects.get_queryset().order_by('id')
    serializer_class = ClientSerializer

    permission_classes = [permissions.IsAuthenticated, ClientPermissions]


class AddressListView(ListCreateAPIView):
    name = 'address-list-view'
    queryset = Address.objects.get_queryset().order_by('id')
    serializer_class = AddressSerializer

    permission_classes = [permissions.IsAuthenticated, AddressPermissions]


class AddressDetail(RetrieveUpdateDestroyAPIView):
    name = 'address-detail'
    queryset = Address.objects.get_queryset().order_by('id')
    serializer_class = AddressSerializer

    permission_classes = [permissions.IsAuthenticated, AddressPermissions]


class AdministratorListView(ListCreateAPIView):
    name = 'administrator-list-view'
    queryset = Administrator.objects.get_queryset().order_by('id')
    serializer_class = AdministratorSerializer
    
    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class AdministratorDetail(RetrieveUpdateDestroyAPIView):
    name = 'administrator-detail'
    queryset = Administrator.objects.get_queryset().order_by('id')
    serializer_class = AdministratorSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class EmployeeListView(ListCreateAPIView):
    name = 'employee-list-view'
    queryset = Employee.objects.get_queryset().order_by('id')
    serializer_class = EmployeeSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class EmployeeDetail(RetrieveUpdateDestroyAPIView):
    name = 'employee-detail'
    queryset = Employee.objects.get_queryset().order_by('id')
    serializer_class = EmployeeSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class StatusListView(ListCreateAPIView):
    name = 'status-list-view'
    queryset = Status.objects.get_queryset().order_by('id')
    serializer_class = StatusSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class StatusDetail(RetrieveUpdateDestroyAPIView):
    name = 'status-detail'
    queryset = Status.objects.get_queryset().order_by('id')
    serializer_class = StatusDetailSerializer
    
    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]
       
    
class GenreListView(ListCreateAPIView):
    name = 'genre-list-view'
    queryset = Genre.objects.get_queryset().order_by('id')
    serializer_class = GenreSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class GenreDetail(RetrieveUpdateDestroyAPIView):
    name = 'genre-detail'
    queryset = Genre.objects.get_queryset().order_by('id')
    serializer_class = GenreSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class AuthorListView(ListCreateAPIView):
    name = 'author-list-view'
    queryset = Author.objects.get_queryset().order_by('id')
    serializer_class = AuthorSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class AuthorDetail(RetrieveUpdateDestroyAPIView):
    name = 'author-detail'
    queryset = Author.objects.get_queryset().order_by('id')
    serializer_class = AuthorSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class WriteListView(ListCreateAPIView):
    name = 'write-list-view'
    queryset = Write.objects.get_queryset().order_by('id')
    serializer_class = WriteSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class WriteDetail(RetrieveUpdateDestroyAPIView):
    name = 'write-detail'
    queryset = Write.objects.get_queryset().order_by('id')
    serializer_class = WriteSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class BookListView(ListCreateAPIView):
    name = 'book-list-view'
    queryset = Book.objects.get_queryset().order_by('id')
    serializer_class = BookSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class BookDetail(RetrieveUpdateDestroyAPIView):
    name = 'book-detail'
    queryset = Book.objects.get_queryset().order_by('id')
    serializer_class = BookSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions]


class SaleListView(ListCreateAPIView):
    name = 'sale-list-view'
    queryset = Sale.objects.get_queryset().order_by('id')
    serializer_class = SaleSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions | 
    SalePermissions]


class SaleDetail(RetrieveUpdateDestroyAPIView):
    name = 'sale-detail'
    queryset = Sale.objects.get_queryset().order_by('id')
    serializer_class = SaleDetailSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions | 
    SalePermissions]


class ItemsaleListView(ListCreateAPIView):
    name = 'itemsale-list-view'
    queryset = Itemsale.objects.get_queryset().order_by('id')
    serializer_class = ItemsaleSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions | 
    ItemsalePermissions]


class ItemsaleDetail(RetrieveUpdateDestroyAPIView):
    name = 'itemsale-detail'
    queryset = Itemsale.objects.get_queryset().order_by('id')
    serializer_class = ItemsaleSerializer

    permission_classes = [permissions.IsAuthenticated, 
    permissions.IsAdminUser | AdministratorPermissions | 
    ItemsalePermissions]


class ApiRoot(GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):

        data = {
            
            "users": reverse(UserListView.name, request=request),
            "address": reverse(AddressListView.name, request=request),
            "clients": reverse(ClientListView.name, request=request),
            "administrators": reverse(AdministratorListView.name, request=request),
            "employees": reverse(EmployeeListView.name, request=request),
            "status": reverse(StatusListView.name, request=request),
            "genres": reverse(GenreListView.name, request=request),
            "authors": reverse(AuthorListView.name, request=request),
            "books": reverse(BookListView.name, request=request),
            "writes": reverse(WriteListView.name, request=request),
            "sales": reverse(SaleListView.name, request=request),
            "itemsales": reverse(ItemsaleListView.name, request=request),
        }
        
        return Response(data, status=status.HTTP_200_OK)