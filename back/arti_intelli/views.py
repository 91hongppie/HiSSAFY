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
import cv2


# Create your views here.
class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)



class Recognition(APIView):
    """
        얼굴 인식
    """
    def post(self, request):
        image = request.FILES['pic_name']
        image1 = fr.load_image_file(image)
        top, right, bottom, left = fr.face_locations(image1)[0]
        image_face = image1[top:bottom, left:right]
        unknown_face = fr.face_encodings(image_face)
        dis = 1
        count = 0
        region_name = request.data.get('region')
        with open(f'data/accounts_{region_name}.json') as accounts:
            datas = json.load(accounts)
        for student_id, data in datas.items():
            for dt in data:
                count += 1
                dt = [np.asarray(dt)]
                distance = fr.face_distance(dt, unknown_face[0])
                if distance < dis and distance < 0.5:
                    if not Check.objects.filter(student_info=student_id):
                        dis = distance
                        account_student_id = student_id
        accounts = Account.objects.filter(student_id=account_student_id)
        student_id = accounts[0].student_id
        serializer = AccountSerializer(accounts[0])
        return Response(serializer.data)


class AddAccount(APIView):
    """
        사용자계정 추가
    """
    def post(self, request):
        student_id = request.data.get('student_id')
        if Account.objects.filter(student_id=student_id):
            return 
        image_name = request.FILES['pic_name']
        known_image = fr.load_image_file(image_name)
        top, right, bottom, left = fr.face_locations(known_image)[0]
        known_image_face = known_image[top:bottom, left:right]
        known_face = fr.face_encodings(known_image_face)
        info = request.data
        json_data = {}
        encodedNumpyData = json.dumps(json_data, cls=NumpyArrayEncoder)
        region_name = info.get('region')
        region = Campus.objects.filter(campus=region_name)[0]
        try:
            with open(f'data/accounts_{region_name}.json') as accounts:
                data = json.load(accounts)
            if info.get('student_id') in data:
                data[info.get('student_id')].append(known_face[0].tolist())
            else:
                data[info.get('student_id')] = [known_face[0].tolist()]
        except:
            data = {}
            data[info.get('student_id')] = [known_face[0].tolist()]

        with open(f'data/accounts_{region_name}.json', 'w', encoding='utf-8') as accounts:
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
        data = serializer.data
        data['face_encodings'] = [known_face[0].tolist()]
        return Response(data)



@api_view(['POST', ])
def add_data(request):
    """
        본인인증 후 데이터 추가
    """
    region_id = request.data.get('region')
    student_id = request.data.get('student_id')
    face_encodings = request.data.get('face_encodings')
    region_name = Campus.objects.filter(id=region_id)
    campus = region_name.get('campus')
    with open(f'data/accounts_{campus}.json') as accounts:
        data = json.load(accounts)
    data[student_id].append(face_encodings)
    return Response(request.data)


@api_view(['POST', ])
def add_campus(request):
    """
        캠퍼스 추가
    """
    data = {
        'campus': request.data.get('campus')
    }
    serializer = CampusSerializer(data=data)
    if serializer.is_valid():
        campus = serializer.save()
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
        전체 교육생 출결정보 목록
    """
    checks = Check.objects.all()
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def check_on_month(request, pk1, pk2, pk3):
    """
        당월 교육생 출결정보 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(date__year=date.today().year, date__month=date.today().month, student_info__stage=pk1, 
        student_info__region=pk2, student_info__classes=pk3).select_related('student_info').order_by('date', 'student_info__name')
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def check_on_daily(request, pk1, pk2, pk3):
    """
        일일 교육생 출결정보 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(date__year=date.today().year, date__month=date.today().month, date__day=date.today().day, 
        student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3).select_related('student_info').order_by('student_info__name')
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def check_on_daily_on_campus(request, pk1):
    """
        지역별 Daily 교육생 출결사항 목록 (region)
    """
    checks = Check.objects.filter(date__year=date.today().year, date__month=date.today().month, date__day=date.today().day, 
        student_info__region=pk1).select_related('student_info').order_by('student_info__name')
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_inclick(request, pk1, pk2, pk3):
    """
        일일 입실 미클릭 교육생 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, in_time__isnull=True, date=date.today())
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_outclick(request, pk1, pk2, pk3):
    """
        일일 퇴실 미클릭 교육생 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, out_time__isnull=True, date=date.today())
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def not_allclick(request, pk1, pk2, pk3):
    """
        일일 결석 교육생 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, in_time__isnull=True, out_time__isnull=True, date=date.today())
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['GET'])
def classes_attendance(request, pk1, pk2, pk3):
    """
        당월 반별 출결현황 (stage, region, classes)
    """
    data = []
    for day in range(1, 32):
        total_persons = Check.objects.filter(date__year=date.today().year, date__month=date.today().month, date__day=day,
            student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3).aggregate(Count('id'))['id__count']
        attend_persons = Check.objects.filter(date__year=date.today().year, date__month=date.today().month, date__day=day,
            student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, in_time__isnull=False).aggregate(Count('id'))['id__count']
        if total_persons != 0:
            days = {
                'day': day,
                'total_persons': total_persons,
                'attend_persons': attend_persons
            }
            data.append(days)    
    return Response(data)


@api_view(['GET'])
def student_attendance(request, pk1, pk2, pk3):
    """
        월별 개인 출결현황 (year, month, student_id)
    """
    checks = Check.objects.filter(date__year=pk1, date__month=pk2, student_info__student_id=pk3)
    class_days = checks.aggregate(Count('id'))['id__count']
    attend_day = checks.filter(in_time__isnull=False).aggregate(Count('id'))['id__count']
    normal_attend_day = checks.filter(in_time__isnull=False, is_late=0, is_early_left=0).aggregate(Count('id'))['id__count']
    come_late_cnt = checks.filter(in_time__gte='09:00:00').aggregate(Count('id'))['id__count']
    early_left_cnt = checks.filter(out_time__range=('14:00:01', '17:59:59')).aggregate(Count('id'))['id__count']
    not_attend_day = checks.filter(in_time__isnull=True, out_time__isnull=True).aggregate(Count('id'))['id__count']
    Disallow_absent_day = checks.filter(in_time__isnull=True, out_time__isnull=True, status=1).aggregate(Count('id'))['id__count']
    allow_absent_day = checks.filter(in_time__isnull=True, out_time__isnull=True, status=2).aggregate(Count('id'))['id__count']
    public_vacation_day = checks.filter(in_time__isnull=True, out_time__isnull=True, status=3).aggregate(Count('id'))['id__count']
    attendance_rate = ((class_days - not_attend_day) / class_days) * 100
    education_costs = ((class_days - Disallow_absent_day) / class_days) * 1000000
    data = {
        'class_days': class_days,
        'attend_day': attend_day,
        'normal_attend_day': normal_attend_day,
        'come_late_cnt': come_late_cnt,
        'early_left_cnt': early_left_cnt,
        'not_attend_day': not_attend_day,
        'public_vacation_day': public_vacation_day,
        'allow_absent_day': allow_absent_day,
        'Disallow_absent_day': Disallow_absent_day,
        'attendance_rate': attendance_rate,
        'education_costs': education_costs
    }
    return Response(data)


@api_view(['PATCH'])
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

