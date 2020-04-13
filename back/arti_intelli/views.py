from django.shortcuts import render
from .models import Campus, Account
from matplotlib import pyplot as plt
from .models import Account, Campus, Check
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serailizers import AccountSerializer
from .models import Account
import face_recognition as fr
import jwt

# Create your views here.

def recognition(request):
    image = request.data.get('image')
    return request

# Create your views here.
def account_list(request):
    accounts = Account.objects.all()
    serializers = AccountSerializer(accounts, many=True)
    return Response(serializers.data)

