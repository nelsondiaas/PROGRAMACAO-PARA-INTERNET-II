from rest_framework import serializers
from game.models import Game

# Convert for Json

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ('id', 'name', 'release_date', 'game_category', 'created')

    