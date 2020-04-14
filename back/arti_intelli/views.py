from django.shortcuts import render
<<<<<<< HEAD
from .models import Campus, Account, Check
from matplotlib import pyplot as plt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import AccountSerializer
=======
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Campus, Account, Check
from .serailizers import AccountSerializer
from matplotlib import pyplot as plt
>>>>>>> 02514b7a924639a11f3fa9286ade130fd910c6e0
import face_recognition as fr

# Create your views here.
def account_list(request):
    accounts = Account.objects.all()
    serializers = AccountSerializer(accounts, many=True)
    return Response(serializers.data)


def recognition(request):
    image = request.data.get('image')
    return request
