from rest_framework.generics import *
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


class EmployeeListView(ListCreateAPIView):
    name = 'employee-list-view'
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeDetail(RetrieveUpdateDestroyAPIView):
    name = 'employee-detail'
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class StatusListView(ListCreateAPIView):
    name = 'status-list-view'
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StatusDetail(RetrieveUpdateDestroyAPIView):
    name = 'status-detail'
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class GenreListView(ListCreateAPIView):
    name = 'genre-list-view'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetail(RetrieveUpdateDestroyAPIView):
    name = 'genre-detail'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class AuthorListView(ListCreateAPIView):
    name = 'author-list-view'
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class AuthorDetail(RetrieveUpdateDestroyAPIView):
    name = 'author-detail'
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class WriteListView(ListCreateAPIView):
    name = 'write-list-view'
    queryset = Write.objects.all()
    serializer_class = WriteSerializer


class WriteDetail(RetrieveUpdateDestroyAPIView):
    name = 'write-detail'
    queryset = Write.objects.all()
    serializer_class = WriteSerializer


class BookListView(ListCreateAPIView):
    name = 'book-list-view'
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookDetail(RetrieveUpdateDestroyAPIView):
    name = 'book-detail'
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class SaleListView(ListCreateAPIView):
    name = 'sale-list-view'
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class SaleDetail(RetrieveUpdateDestroyAPIView):
    name = 'sale-detail'
    queryset = Sale.objects.all()
    serializer_class = SaleDetailSerializer


class ItemsaleListView(ListCreateAPIView):
    name = 'itemsale-list-view'
    queryset = Itemsale.objects.all()
    serializer_class = ItemsaleSerializer


class ItemsaleDetail(RetrieveUpdateDestroyAPIView):
    name = 'itemsale-detail'
    queryset = Itemsale.objects.all()
    serializer_class = ItemsaleSerializer


class ApiRoot(GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):

        data = {
            
            "address": reverse(AddressListView.name, request=request),
            "clients": reverse(ClientListView.name, request=request),
            "administrators": reverse(AdministratorListView.name, request=request),
            "employee": reverse(EmployeeListView.name, request=request),
            "status": reverse(StatusListView.name, request=request),
            "genres": reverse(GenreListView.name, request=request),
            "authors": reverse(AuthorListView.name, request=request),
            "books": reverse(BookListView.name, request=request),
            "write": reverse(WriteListView.name, request=request),
            "sales": reverse(SaleListView.name, request=request),
            "itemsales": reverse(ItemsaleListView.name, request=request),
        }
        
        return Response(data, status=status.HTTP_200_OK)