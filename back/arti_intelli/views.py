from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Campus, Account, Check
from .serailizers import AccountSerializer
from matplotlib import pyplot as plt
import face_recognition as fr

# Create your views here.
def account_list(request):
    accounts = Account.objects.all()
    serializers = AccountSerializer(accounts, many=True)
    return Response(serializers.data)


def recognition(request):
    image = request.data.get('image')
    return request
