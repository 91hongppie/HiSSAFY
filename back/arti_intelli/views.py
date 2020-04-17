from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Campus, Account, Check, Face
from .serializers import CampusSerializer, AccountSerializer, CheckSerializer, FaceSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
import datetime
from rest_framework.parsers import MultiPartParser, FileUploadParser
from matplotlib import pyplot as plt
from PIL import Image
# from gpuinfo import GPUInfo
import numpy as np
from numpy import genfromtxt
import face_recognition as fr
# import pandas as pd
import csv
import ast


# Create your views here.
def test(request):
    user = User.objects.all()
    context = {'user': user}
    print(user[0].password)
    return render(request, 'arti_intelli/test.html', context)


class Recognition(APIView):
    def post(self, request):
        image = request.FILES['pic_name']
        image = fr.load_image_file(image)
        top, right, bottom, left = fr.face_locations(image)[0]
        image_face = image[top:bottom, left:right]
        unknown_face = fr.face_encodings(image_face)
        dis = 1
        face_pics = Face.objects.all()
        for face_pic in face_pics:
            image_1 = fr.load_image_file(face_pic.pic_name)
            image_face_1 = image_1[face_pic.top:face_pic.bottom, face_pic.left:face_pic.right]
            known_face = fr.face_encodings(image_face_1)
            distance = fr.face_distance(known_face, unknown_face[0])
            if distance < dis and distance < 0.5:
                dis = distance
                account_student_id = face_pic.account_id
        accounts = Account.objects.filter(id=account_student_id)
        serializer = AccountSerializer(accounts[0])
        return Response(serializer.data)


class AddAccount(APIView):
    def post(self, request):
        image_name = request.FILES['pic_name']
        print(image_name.file)
        known_image = fr.load_image_file(image_name)
        top, right, bottom, left = fr.face_locations(known_image)[0]
        known_image_face = known_image[top:bottom, left:right]
        known_face = fr.face_encodings(known_image_face)
        info = request.data
        region = Campus.objects.filter(campus=info.get('region'))[0]
        data = {
            'pic_name': image_name,
            'name': info.get('name'),
            'stage': info.get('stage'),
            'classes': info.get('classes'),
            'birthday': info.get('birthday'),
            'student_id': info.get('student_id'),
            'region': region.idWS
        }
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            account = serializer.save()
        face_data = {
            'pic_name': image_name,
            'top': top,
            'bottom': bottom,
            'right': right,
            'left': left,
            'account': account.id
        }
        serializer1 = FaceSerializer(data=face_data)
        if serializer1.is_valid():
            face = serializer1.save()
        return Response(serializer.data)


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
# @permission_classes([IsAuthenticated])
# @authentication_classes([JSONWebTokenAuthentication])
def in_calling(request):
    """
        입실 클릭
    """
    students = Account.objects.get(name=request.user)['student_id']
    checks = Check.objects.get(student_info=students)
    serializers = CheckSerializer(checks, many=True)
    if serializers.is_valid():
        serializers.save(in_time=datetime.time.now())
    return Response(serializers.data)


@api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JSONWebTokenAuthentication])
def out_calling(request):
    """
        퇴실 클릭
    """
    students = Account.objects.get(name=request.user)['student_id']
    checks = Check.objects.filter(student_info=students)
    serializers = CheckSerializer(checks, many=True)
    if serializers.is_valid():
        serializers.save(in_time=datetime.time.now())
    return Response(serializers.data)

