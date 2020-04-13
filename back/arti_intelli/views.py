from django.shortcuts import render
<<<<<<< HEAD
from .models import Campus, Account
from matplotlib import pyplot as plt
from .models import Account, Campus, Check
from Ipython.
import face_recognition as fr

# Create your views here.

def recognition(request):
    image = request.data.get('image')
    return request
=======
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

>>>>>>> c6f83cc99d2d400f4d5c453988275cd1b6969a2d
