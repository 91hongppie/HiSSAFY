from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Campus, Account, Check
from .serializers import CampusSerializer, AccountSerializer, CheckSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import datetime
from matplotlib import pyplot as plt
import face_recognition as fr


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
    checks = Check.objects.filter(in_time__isnull=True).select_related('student_info')
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_outclick(request):
    """
        퇴실 미클릭 교육생 목록
    """
    checks = Check.objects.filter(out_time__isnull=True).select_related('student_info')
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_allclick(request):
    """
        결석 교육생 목록
    """
    checks = Check.objects.filter(in_time__isnull=True, out_time__isnull=True).select_related('student_info')
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
# @authentication_classes([JSONWebTokenAuthentication])
def in_calling(request):
    """
        입실 클릭
    """
    checks = Check.objects.filter(request.user, data=request.data)
    serializers = CheckSerializer(checks, many=True)
    if serializers.is_valid():
        serializers.save(in_time=datetime.datetime.now())
    return Response(serializers.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
# @authentication_classes([JSONWebTokenAuthentication])
def out_calling(request):
    """
        퇴실 클릭
    """
    serializers = CheckSerializer(request.user, data=request.data)
    if serializers.is_valid():
        serializers.save(in_time=datetime.datetime.now())
    return Response(serializers.data)


@api_view(['GET'])
def recognition(request):
    """
        얼굴 인식
    """
    image = request.data.get('image')
    return request
