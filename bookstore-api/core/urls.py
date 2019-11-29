from django.urls import path
from .views import *


urlpatterns = [

    path('', ApiRoot.as_view(), name=ApiRoot.name),

    path('address/', AddressListView.as_view(), name=AddressListView.name),
    path('address/<int:pk>/', AddressDetail.as_view(), name=AddressDetail.name),

    path('clients/', ClientListView.as_view(), name=ClientListView.name),
    path('clients/<int:pk>/', ClientDetail.as_view(), name=ClientDetail.name),

    path('administrators/', AdministratorListView.as_view(), name=AdministratorListView.name),
    path('administrators/<int:pk>/', AdministratorDetail.as_view(), name=AdministratorDetail.name),

    path('employees/', EmployeeListView.as_view(), name=EmployeeListView.name),
    path('employees/<int:pk>/', EmployeeDetail.as_view(), name=EmployeeDetail.name),

    path('status/', StatusListView.as_view(), name=StatusListView.name),
    path('status/<int:pk>/', StatusDetail.as_view(), name=StatusDetail.name),

    path('genres/', GenreListView.as_view(), name=GenreListView.name),
    path('genres/<int:pk>/', GenreDetail.as_view(), name=GenreDetail.name),

    path('authors/', AuthorListView.as_view(), name=AuthorListView.name),
    path('authors/<int:pk>/', AuthorDetail.as_view(), name=AuthorDetail.name),
    
    path('writes/', WriteListView.as_view(), name=WriteListView.name),
    path('writes/<int:pk>/', WriteDetail.as_view(), name=WriteDetail.name),

    path('books/', BookListView.as_view(), name=BookListView.name),
    path('books/<int:pk>/', BookDetail.as_view(), name=BookDetail.name),

    path('sales/', SaleListView.as_view(), name=SaleListView.name),
    path('sales/<int:pk>/', SaleDetail.as_view(), name=SaleDetail.name),

    path('itemsales/', ItemsaleListView.as_view(), name=ItemsaleListView.name),
    path('itemsales/<int:pk>/', ItemsaleDetail.as_view(), name=ItemsaleDetail.name),

]