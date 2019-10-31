from rest_framework import serializers
from accounts.models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'owner', 'balance', 'creation_date', 'createdAt', 'updatedAt']
    
    def verify_balance(self, serializer):
         if serializer.is_valid():
            if self.verify_date(serializer):
                if serializer.validated_data['balance'] < 0:
                    raise serializers.ValidationError("Negative balance")
                return True

    def verify_date(self, serializer):
        try:
            if serializer.validated_data['creation_date']:
                raise serializers.ValidationError("Date cannot be applied")
        except KeyError:
            return True

    def add_credit(self, serializer, instance):
        if serializer.is_valid():
            if serializer.validated_data['balance'] == 0:
                raise serializers.ValidationError("Value is zero, operation denied")
            elif serializer.validated_data['balance'] > 0:
                instance.balance += serializer.validated_data['balance']
                instance.save()
                return True
            else:   
                instance.balance += serializer.validated_data['balance']
                if instance.balance > 0:
                    instance.save()
                    return False
                raise serializers.ValidationError("Insuficient balance")


    