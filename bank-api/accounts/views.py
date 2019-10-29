from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import AccountSerializer
from rest_framework import status
from django.http import Http404
from accounts.models import Account

# Create your views here.

class AccountCreateOrList(APIView):
    
    def post(self, request, format=None):
        account_serializer = AccountSerializer(data=request.data)
        if account_serializer.verify_balance(account_serializer, request.data):
            account_serializer.save()
            return Response(account_serializer.data, status=status.HTTP_201_CREATED)
        return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, format=None):
        account = Account.objects.all()
        account_serializer = AccountSerializer(account, many=True)
        return Response(account_serializer.data)

class AccountDetail(APIView):
    
    def get_object(self, pk):
        try:
            return Account.objects.get(pk=pk)
        except Account.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        account = self.get_object(pk)
        account_serializer = AccountSerializer(account)
        return Response(account_serializer.data)

    def put(self, request, pk, format=None):
        account = self.get_object(pk)
        account_serializer = AccountSerializer(account, data=request.data)
        if account_serializer.verify_balance(account_serializer, request.data):
            account_serializer.save()
            return Response(account_serializer.data)
        return Response(account_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk, format=None):
        account = self.get_object(pk)
        account_serializer = AccountSerializer(account, data=request.data)
        if account_serializer.add_credit(account_serializer, request.data, account):
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk, format=None):
        account_serializer = AccountSerializer(data=request.data)
        account = self.get_object(pk)
        if account_serializer.is_valid():
            account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)