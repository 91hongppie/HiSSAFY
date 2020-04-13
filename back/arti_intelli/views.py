from django.shortcuts import render
from .models import Campus, Account
from matplotlib import pyplot as plt
from .models import Account, Campus, Check
from Ipython.
import face_recognition as fr

# Create your views here.

def recognition(request):
    image = request.data.get('image')
    return request
