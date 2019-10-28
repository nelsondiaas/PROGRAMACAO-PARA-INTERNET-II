from django.conf.urls import url
from game import views

# Router

urlpatterns = [
    
    url('api/v1/games/', views.game_create),
    url('api/v1/games/', views.game_list),
    url('api/v1/games/<int:id>/', views.game_detail)

]