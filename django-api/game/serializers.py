from rest_framework import serializers
from django.utils import timezone
from datetime import datetime
from game.models import Game

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'release_date', 'game_category', 'created', 'createdAt', 'updatedAt']
    
    def verify_exists(self, serializer, data):
        if serializer.is_valid():
            exists = Game.objects.filter(name=data['name']).exists()
            if exists: raise serializers.ValidationError("That name already exists!")
            return True

    def verify_releases(self, data):
        if data.release_date <= timezone.make_aware(datetime.now(), timezone.get_current_timezone()):
            raise serializers.ValidationError("This game has been released, you cannot delete")
        return True

        