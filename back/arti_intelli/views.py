from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Campus, Account, Check
from .serializers import CampusSerializer, AccountSerializer, CheckSerializer
from matplotlib import pyplot as plt
import face_recognition as fr
# import jwt

# Create your views here.
@api_view(['GET'])
def campus_list(request):
    """
        캠퍼스 목록
    """
    campus = Campus.objects.all()
    serializers = CampusSerializer(campus, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def account_list(request):
    """
        교육생 목록
    """
    accounts = Account.objects.all()
    serializers = AccountSerializer(accounts, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def check_on(request):
    """
        전체 교육생 출결사항 목록
    """
    checks = Check.objects.all()
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_inclick(request):
    """
        입실 미클릭 교육생 목록
    """
    checks = Check.objects.all()
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_outclick(request):
    """
        퇴실 미클릭 교육생 목록
    """
    checks = Check.objects.all()
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def recognition(request):
    """
        얼굴 인식
    """
    image = request.data.get('image')
    return request
