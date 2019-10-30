from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from game.serializers import GameSerializer
from rest_framework import status
from django.http import Http404
from game.models import Game

# Create your views here.

class GameCreateOrList(APIView):
    
    def post(self, request, format=None):
        game_serializer = GameSerializer(data=request.data)
        if game_serializer.verify_exists(game_serializer):
            game_serializer.save()
            return Response(game_serializer.data, status=status.HTTP_201_CREATED)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        games = Game.objects.all()
        games_serializer = GameSerializer(games, many=True)
        return Response(games_serializer.data)

class GameDetail(APIView):

    def get_object(self, pk):
        try:
            return Game.objects.get(pk=pk)
        except Game.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        game = self.get_object(pk)
        game_serializer = GameSerializer(game)
        return Response(game_serializer.data)

    def put(self, request, pk, format=None):
        game = self.get_object(pk)
        game_serializer = GameSerializer(game, data=request.data)
        if game_serializer.verify_exists(game_serializer):
            game_serializer.save()
            return Response(game_serializer.data)
        return Response(game_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        game_serializer = GameSerializer(data=request.data)
        game = self.get_object(pk)
        if game_serializer.verify_releases(game):
            game.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        