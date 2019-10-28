from django.urls import path
from accounts import views

# Router

urlpatterns = [
    
    path('api/v1/accounts/', views.AccountCreateOrList.as_view()),
    path('api/v1/accounts/<int:pk>/', views.AccountDetail.as_view())

]