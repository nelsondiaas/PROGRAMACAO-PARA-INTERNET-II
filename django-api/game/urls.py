from django.urls import path
from game import views

# Router

urlpatterns = [
    
    path('api/v1/games/', views.GameCreateOrList.as_view()),
    path('api/v1/games/<int:pk>/', views.GameDetail.as_view())

]