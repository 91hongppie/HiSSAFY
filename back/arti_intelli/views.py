from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Campus, Account, Check
from .serializers import CampusSerializer, AccountSerializer, CheckSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from datetime import datetime, date, time
from django.db.models import Count
from rest_framework.parsers import MultiPartParser, FileUploadParser
from matplotlib import pyplot as plt
from PIL import Image
# from gpuinfo import GPUInfo
import numpy as np
from numpy import genfromtxt
import face_recognition as fr
import json
from json import JSONEncoder

# import pandas as pd
import csv
import ast


class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)


# Create your views here.
def test(request):
    user = User.objects.all()
    context = {'user': user}
    print(user[0].password)
    return render(request, 'arti_intelli/test.html', context)


class Recognition(APIView):
    """
        얼굴 인식
    """
    def post(self, request):
        image = request.FILES['pic_name']
        image = fr.load_image_file(image)
        top, right, bottom, left = fr.face_locations(image)[0]
        image_face = image[top:bottom, left:right]
        unknown_face = fr.face_encodings(image_face)
        dis = 1
        with open('accounts_대전.json') as accounts:
            datas = json.load(accounts)
        for student_id, data in datas.items():
            for dt in data:
                dt = [np.asarray(dt)]
                distance = fr.face_distance(dt, unknown_face[0])
                print(student_id)
                if distance < dis and distance < 0.5:
                    dis = distance
                    account_student_id = student_id
        accounts = Account.objects.filter(student_id=account_student_id)
        serializer = AccountSerializer(accounts[0])
        return Response(serializer.data)


class AddAccount(APIView):
    """
        사용자계정 추가
    """
    def post(self, request):
        image_name = request.FILES['pic_name']
        known_image = fr.load_image_file(image_name)
        top, right, bottom, left = fr.face_locations(known_image)[0]
        known_image_face = known_image[top:bottom, left:right]
        known_face = fr.face_encodings(known_image_face)
        print(known_face)
        info = request.data
        json_data = {}
        encodedNumpyData = json.dumps(json_data, cls=NumpyArrayEncoder)
        region_name = info.get('region')
        region = Campus.objects.filter(campus=region_name)[0]
        with open(f'accounts_{region_name}.json') as accounts:
            data = json.load(accounts)
        if info.get('student_id') in data:
            data[info.get('student_id')].append(known_face[0].tolist())
        else:
            data[info.get('student_id')] = [known_face[0].tolist()]
        with open(f'accounts_{region_name}.json', 'w', encoding="utf-8") as accounts:
            json.dump(data, accounts, cls=NumpyArrayEncoder, ensure_ascii=False, indent=2)
        data = {
            'pic_name': image_name,
            'name': info.get('name'),
            'stage': info.get('stage'),
            'classes': info.get('classes'),
            'birthday': info.get('birthday'),
            'student_id': info.get('student_id'),
            'region': region.id
        }
        serializer = AccountSerializer(data=data)
        if serializer.is_valid():
            account = serializer.save()
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
        전체 교육생 목록
    """
    accounts = Account.objects.all()
    serializers = AccountSerializer(accounts, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def account_list_region(request, pk1, pk2):
    """
        기수별, 지역별 교육생 목록
    """
    accounts = Account.objects.filter(stage=pk1, region=pk2).order_by('classes', 'name')
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
def check_on_month(request, pk1, pk2, pk3):
    """
        당월 교육생 출결사항 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(date__year=date.today().year, date__month=date.today().month, student_info__stage=pk1, 
        student_info__region=pk2, student_info__classes=pk3).select_related('student_info').order_by('date', 'student_info__name')
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def check_on_daily(request, pk1, pk2, pk3):
    """
        Daily 교육생 출결사항 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(date__year=date.today().year, date__month=date.today().month, date__day=date.today().day, 
        student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3).select_related('student_info').order_by('student_info__name')
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_inclick(request, pk1, pk2, pk3):
    """
        Daily 입실 미클릭 교육생 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, in_time__isnull=True, date=date.today())
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_outclick(request, pk1, pk2, pk3):
    """
        Daily 퇴실 미클릭 교육생 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, out_time__isnull=True, date=date.today())
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_allclick(request, pk1, pk2, pk3):
    """
        Daily 결석 교육생 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, in_time__isnull=True, out_time__isnull=True, date=date.today())
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def student_attendance(request, pk1, pk2, pk3):
    """
        월별 개인 출결현황 (year, month, student_id)
    """
    checks = Check.objects.filter(date__year=pk1, date__month=pk2, student_info__student_id=pk3)
    attend_day = checks.filter(in_time__isnull=False).aggregate(Count('id'))['id__count']
    come_late_cnt = checks.filter(in_time__gte='09:00:00').aggregate(Count('id'))['id__count']
    early_left_cnt = checks.filter(out_time__range=('14:00:01', '17:59:59')).aggregate(Count('id'))['id__count']
    total_day = checks.aggregate(Count('id'))['id__count']
    not_attend_day = checks.filter(in_time__isnull=True, out_time__isnull=True).aggregate(Count('id'))['id__count']
    attendance_rate = ((total_day - not_attend_day) / total_day) * 100
    data = {
        'attend_day': attend_day,
        'come_late_cnt': come_late_cnt,
        'early_left_cnt': early_left_cnt,
        'not_attend_day': not_attend_day,
        'attendance_rate': attendance_rate
    }
    return Response(data)


@api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JSONWebTokenAuthentication])
def in_calling(request):
    """
        입실 클릭
    """
    students = Account.objects.get(name=request.user)['student_id']
    checks = Check.objects.get(student_info=students)
    serializers = CheckSerializer(checks)
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
    serializers = CheckSerializer(checks)
    if serializers.is_valid():
        serializers.save(in_time=datetime.time.now())
    return Response(serializers.data)

