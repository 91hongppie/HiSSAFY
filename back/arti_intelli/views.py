from django.shortcuts import render
from .models import Campus, Account, Check
from matplotlib import pyplot as plt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AccountSerializer
import face_recognition as fr

# Create your views here.

def recognition(request):
    image = request.data.get('image')
    return request

# Create your views here.
def account_list(request):
    accounts = Account.objects.all()
    serializers = AccountSerializer(accounts, many=True)
    return Response(serializers.data)

