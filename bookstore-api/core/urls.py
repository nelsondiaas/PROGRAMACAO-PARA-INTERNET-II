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

]