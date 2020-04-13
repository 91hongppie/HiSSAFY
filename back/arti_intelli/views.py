from django.shortcuts import render
import jwt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serailizers import AccountSerializer
from .models import Account

# Create your views here.
def account_list(request):
    accounts = Account.objects.all()
    serializers = AccountSerializer(accounts, many=True)
    return Response(serializers.data)

