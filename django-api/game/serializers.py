from rest_framework import serializers
from game.models import Game

# Convert for Json

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'release_date', 'game_category', 'created', 'createdAt', 'updatedAt']
    
     @staticmethod
    def verify_exists(self, serializer, data):
        if serializer.is_valid():
            exists = Game.objects.filter(name=data['name']).exists()
            if exists: raise serializers.ValidationError("That name already exists!")
            return True

    def verify_releases(self, data):
        if game.release_date <= timezone.make_aware(datetime.now(), timezone.get_current_timezone()):
            
        