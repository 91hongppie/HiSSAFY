from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Campus, Account, Check, AccountImage
from .serializers import CampusSerializer, AccountSerializer, CheckSerializer, AccountImageSerializer
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from datetime import datetime, date, time
from django.db.models import Count, Avg
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
        # image = request.FILES['pic_name']
        data_list = []
        try:
            image = request.data['pic_name']
            region_id = request.data['region_id']
            region = Campus.objects.get(id=region_id).campus
            image1 = fr.load_image_file(image)
            faces = fr.face_locations(image1)
            for face in faces:
                top, right, bottom, left = face
                image_face = image1[top:bottom, left:right]
                unknown_face = fr.face_encodings(image_face)
                dis = 1
                # region_name = request.data.get('region')
                with open(f'data/accounts_{region}.json') as accounts:
                    datas = json.load(accounts)
                for student_id, data in datas.items():
                    for dt in data:
                        dt = [np.asarray(dt)]
                        distance = fr.face_distance(dt, unknown_face[0])
                        if distance < dis and distance < 0.5:
                            if not Check.objects.filter(student_info=student_id):
                                dis = distance
                                account_student_id = student_id
                accounts = Account.objects.filter(student_id=account_student_id)
                serializer = AccountSerializer(accounts, many=True)
                data = serializer.data
                # data['face_encodings'] = unknown_face[0].tolist()
                data_list.append(data)
        except:
            return Response(data_list)
        return Response(data_list)


class AddAccount(APIView):
    """
        사용자계정 추가
    """
    def post(self, request):
        student_id = request.data.get('student_id')
        if Account.objects.filter(student_id=student_id):
            return Response('이미 등록된 사용자입니다.')
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
        return Response(serializer.data)


@api_view(['POST', ])
def add_data(request):
    """
        본인인증 후 데이터 추가
    """
    region_id = request.data.get('region')
    student_id = request.data.get('student_id')
    face_encodings = request.data.get('face_encodings')
    region_name = Campus.objects.filter(id=region_id)
    campus = region_name[0].campus
    print(face_encodings)
    print(campus)
    with open(f'data/accounts_{campus}.json') as accounts:
        data = json.load(accounts)
    data[request.data.get('student_id')].append(face_encodings)
    with open(f'data/accounts_{campus}.json', 'w', encoding='utf-8') as accounts:
        json.dump(data, accounts, cls=NumpyArrayEncoder, ensure_ascii=False, indent=2)
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
        당일 전체 교육생 출결여부 목록
    """
    campuss = Campus.objects.all()
    accounts = Account.objects.all()
    datas = {}
    datas['location'] = []
    for campus in campuss:
        datas[campus.id] = {}
        datas['location'].append(campus.campus)
    for account in accounts:
        if not datas[account.region.id].get(account.stage):
            datas[account.region.id][account.stage] = {}
            if not datas[account.region.id][account.stage].get(account.classes):
                datas[account.region.id][account.stage][account.classes] = {'members': 0, 'check': [], 'uncheck': []}
        else:
            if not datas[account.region.id][account.stage].get(account.classes):
                datas[account.region.id][account.stage][account.classes] = {'members': 0, 'check': [], 'uncheck': []}
        if Check.objects.filter(date__year=date.today().year, date__month=date.today().month, date__day=date.today().day, student_info=account.id):
            datas[account.region.id][account.stage][account.classes]['check'].append({'student_id': account.student_id, 'name':account.name})
        else:
            datas[account.region.id][account.stage][account.classes]['uncheck'].append({'student_id': account.student_id, 'name':account.name})
        datas[account.region.id][account.stage][account.classes]['members'] += 1
    return Response(datas)


@api_view(['GET'])
def check_on_month(request, pk1, pk2, pk3, pk4, pk5):
    """
        월별 교육생 출결정보 상세목록(반) (stage, region, classes, year, month)
    """
    accounts = Account.objects.filter(stage=pk1, region=pk2, classes=pk3).order_by('name')
    students = []
    for acc in range(len(accounts)):
        student_id = accounts.values('student_id')[acc]['student_id']
        name = accounts.values('name')[acc]['name']
        if [student_id, name] not in students:
            students.append([student_id, name])
    datas = []
    for student in students:
        checks = Check.objects.filter(date__year=pk4, date__month=pk5, student_info__student_id=student[0])
        class_days = 0
        not_attend_day = 0
        for day in range(1, 32):
            class_day = Check.objects.filter(date__year=pk4, date__month=pk5, date__day=day)
            if class_day:
                class_days += 1
                if not checks.filter(date__day=day):
                    not_attend_day += 1
        come_late_cnt = checks.filter(status=1, in_time__gte='09:00:00').aggregate(Count('id'))['id__count']
        early_left_cnt = checks.filter(status=1, out_time__range=('14:00:01', '17:59:59')).aggregate(Count('id'))['id__count']
        normal_attend_day = checks.filter(in_time__isnull=False, is_late=0, is_early_left=0).aggregate(Count('id'))['id__count']-come_late_cnt-early_left_cnt
        attend_day = class_days - not_attend_day
        public_vacation_day = 0
        allow_absent_day = 0
        Disallow_absent_day = not_attend_day-allow_absent_day-public_vacation_day
        try:
            attendance_rate = '{:.0f}'.format(((class_days - not_attend_day) / class_days) * 100)
            education_costs = '{:.0f}'.format(((class_days - Disallow_absent_day - allow_absent_day) / class_days) * 1000000)
        except ZeroDivisionError:
            attendance_rate = 0
            education_costs = 0
        data = {
            'student_id': student[0],
            'name': student[1],
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
        datas.append(data)
    return Response(datas)


@api_view(['GET'])
def check_on_month_one(request, pk1, pk2, pk3):
    """
        월별 교육생 출결정보 상세목록(개인) (student_id, year, month)
    """
    student_id = pk1
    name = Account.objects.filter(student_id=pk1).values('name')[0]['name']
    datas = []
    checks = Check.objects.filter(date__year=pk2, date__month=pk3, student_info__student_id=pk1)
    class_days = 0
    not_attend_day = 0
    for day in range(1, 32):
        class_day = Check.objects.filter(date__year=pk2, date__month=pk3, date__day=day)
        if class_day:
            class_days += 1
            if not checks.filter(date__day=day):
                not_attend_day += 1
    come_late_cnt = checks.filter(status=1, in_time__gte='09:00:00').aggregate(Count('id'))['id__count']
    early_left_cnt = checks.filter(status=1, out_time__range=('14:00:01', '17:59:59')).aggregate(Count('id'))['id__count']
    normal_attend_day = checks.filter(in_time__isnull=False, is_late=0, is_early_left=0).aggregate(Count('id'))['id__count']-come_late_cnt-early_left_cnt
    attend_day = class_days - not_attend_day
    public_vacation_day = 0
    allow_absent_day = 0
    Disallow_absent_day = not_attend_day-allow_absent_day-public_vacation_day
    try:
        attendance_rate = '{:.0f}'.format(((class_days - not_attend_day) / class_days) * 100)
        education_costs = '{:.0f}'.format(((class_days - Disallow_absent_day - allow_absent_day) / class_days) * 1000000)
    except ZeroDivisionError:
        attendance_rate = 0
        education_costs = 0
    data = {
        'student_id': student_id,
        'name': name,
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
    datas.append(data)
    return Response(datas)


@api_view(['GET'])
def check_on_daily(request, pk1, pk2, pk3):
    """
        당일 교육생 출결정보 상세목록 (stage, region, classes)
    """
    account = Account.objects.filter(stage=pk1, region=pk2, classes=pk3).order_by('name')
    a_datas = AccountSerializer(account, many=True)
    accounts = a_datas.data
    students = []
    for acc in accounts:
        if [acc['student_id'], acc['name']] not in students:
            students.append([acc['student_id'], acc['name']])
    data = []
    for student in students:
        checks = Check.objects.filter(date=date.today(), student_info__stage=pk1, student_info__region=pk2, 
            student_info__classes=pk3, student_info__student_id=student[0])
        if checks:
            serializers = CheckSerializer(checks, many=True)
            c_datas = serializers.data
            for c_data in c_datas:
                students = account.filter(id=c_data['student_info_id'])
                name = students.values('name')[0]['name']
                student_id = students.values('student_id')[0]['student_id']
                datas = {
                    'student_id': student_id,
                    'name': name,
                    'date': c_data['date'],
                    'in_time': c_data['in_time'],
                    'out_time': c_data['out_time'],
                    'is_late': c_data['is_late'],
                    'is_early_left': c_data['is_early_left'],
                    'status': c_data['status']
                }
                data.append(datas)
        else:
            datas = {
                'student_id': student[0],
                'name': student[1],
                'date': date.today(),
                'in_time': None,
                'out_time': None,
                'is_late': False,
                'is_early_left': False,
                'status': 0
            }
            data.append(datas)
    return Response(data)


@api_view(['GET'])
def not_inclick(request, pk1, pk2, pk3):
    """
        당일 입실 미클릭 교육생 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, in_time__isnull=True, 
        date=date.today()).order_by('student_info__name')
    serializers = CheckSerializer(checks, many=True)
    c_datas = serializers.data
    data = []
    accounts = Account.objects.filter(region=pk1)
    for c_data in c_datas:
        students = accounts.filter(id=c_data['student_info_id'])
        name = students.values('name')[0]['name']
        student_id = students.values('student_id')[0]['student_id']
        datas = {
            'id': c_data['id'],
            'student_id': student_id,
            'name': name,
            'date': c_data['date'],
            'in_time': c_data['in_time'],
            'out_time': c_data['out_time']
        }
        data.append(datas)
    return Response(data)


@api_view(['GET'])
def not_outclick(request, pk1, pk2, pk3):
    """
        당일 퇴실 미클릭 교육생 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, in_time__isnull=False, 
        out_time__isnull=True, date=date.today()).order_by('student_info__name')
    serializers = CheckSerializer(checks, many=True)
    c_datas = serializers.data
    data = []
    accounts = Account.objects.filter(region=pk1)
    for c_data in c_datas:
        students = accounts.filter(id=c_data['student_info_id'])
        name = students.values('name')[0]['name']
        student_id = students.values('student_id')[0]['student_id']
        datas = {
            'id': c_data['id'],
            'student_id': student_id,
            'name': name,
            'date': c_data['date'],
            'in_time': c_data['in_time'],
            'out_time': c_data['out_time']
        }
        data.append(datas)
    return Response(data)


@api_view(['GET'])
def not_allclick(request, pk1, pk2, pk3):
    """
        당일 결석 교육생 목록 (stage, region, classes)
    """
    checks = Check.objects.filter(student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, in_time__isnull=True, 
        out_time__isnull=True, date=date.today()).order_by('student_info__name')
    serializers = CheckSerializer(checks, many=True)
    c_datas = serializers.data
    data = []
    accounts = Account.objects.filter(region=pk1)
    for c_data in c_datas:
        students = accounts.filter(id=c_data['student_info_id'])
        name = students.values('name')[0]['name']
        student_id = students.values('student_id')[0]['student_id']
        datas = {
            'id': c_data['id'],
            'student_id': student_id,
            'name': name,
            'date': c_data['date'],
            'in_time': c_data['in_time'],
            'out_time': c_data['out_time']
        }
        data.append(datas)
    return Response(data)


@api_view(['GET'])
def classes_attendance(request, pk1, pk2, pk3):
    """
        당월 날짜별, 월평균 출석률 (stage, region, classes)
    """
    account = Account.objects.filter(stage=pk1, region=pk2, classes=pk3).order_by('name')
    a_datas = AccountSerializer(account, many=True)
    accounts = a_datas.data
    students = []
    for acc in accounts:
        if [acc['student_id']] not in students:
            students.append(acc['student_id'])
    datas = []
    avg_attendance_rate = 0
    cnt = 0
    for day in range(1, 32):
        total_persons = len(students)
        attend_persons = Check.objects.filter(date__year=date.today().year, date__month=date.today().month, date__day=day,
            student_info__stage=pk1, student_info__region=pk2, student_info__classes=pk3, in_time__isnull=False, status=True).aggregate(Count('id'))['id__count']
        attendance_rate = '{:.0f}'.format((attend_persons / total_persons) * 100)
        checks = Check.objects.filter(date__year=date.today().year, date__month=date.today().month, date__day=day)
        if checks:
            days = {
                'day': day,
                'total_persons': total_persons,
                'attend_persons': attend_persons,
                'attendance_rate': attendance_rate
            }
            datas.append(days)
            avg_attendance_rate += int(attendance_rate)
            cnt += 1
    avg_attendance_rate = avg_attendance_rate / cnt
    data = {'avg_attendance_rate': '{:.0f}'.format(avg_attendance_rate)}
    datas.append(data)
    return Response(datas)


@api_view(['POST'])
def in_calling(request):
    """
        입실 클릭
    """
    student_id = '0233100'
    students = Account.objects.filter(student_id=student_id)
    student = AccountSerializer(students, many=True).data[0]['id']
    checks = Check.objects.filter(date=date.today(), student_info__student_id=student_id)
    if not checks:
        if datetime.now().time() < '09:00:00':
            Check.objects.create(date=date.today(), in_time=datetime.now().time(), status='1', student_info=Account.objects.get(id=student))
        else:
            Check.objects.create(date=date.today(), in_time=datetime.now().time(), is_late=True, status='1', student_info=Account.objects.get(id=student))
    checks = Check.objects.filter(date=date.today(), student_info__student_id=student_id)
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)


@api_view(['PATCH'])
def out_calling(request):
    """
        퇴실 클릭
    """
    student_id = '0233100'
    checks = Check.objects.filter(date=date.today(), student_info__student_id=student_id)
    if checks:
        if datetime.now().time() >= '18:00:00':
            check.update(out_time=datetime.now().time())
        else:
            if datetime.now().time() >= '14:00:00':
                check.update(out_time=datetime.now().time(), is_early_left=True)
            else:
                check.update(out_time=datetime.now().time(), status=0)
    checks = Check.objects.filter(date=date.today(), student_info__student_id=student_id)
    serializers = CheckSerializer(checks, many=True)
    return Response(serializers.data)

