from django.urls import path
from game import views

# Router

urlpatterns = [
    path('api/v1/game', views.game_create),
    path('api/v1/game/list', views.game_list),
    path('api/v1/game/<int:id>', views.game_detail)

]