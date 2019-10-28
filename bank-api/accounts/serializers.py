from rest_framework import serializers
from accounts.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'owner', 'balance', 'creation_date', 'createdAt', 'updatedAt']
    
    def verify_balance(self, serializer, data):
        if serializer.is_valid():
            if data['balance'] < 0:
                raise serializers.ValidationError("Negative balance")
            return True
            