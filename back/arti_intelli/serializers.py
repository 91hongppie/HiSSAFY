from rest_framework import serializers
from .models import Campus, Account, Check

class CampusSerializer(serializers.ModelSerializer):
    class Meta(Campus):
        model = Campus
        fields = ('id', 'campus',)


class AccountSerializer(serializers.ModelSerializer):
    class Meta(Account):
        model = Account
        fields = ('id', 'pic_name', 'name', 'stage', 'classes', 'birthday', 'student_id', 'region',)


class CheckSerializer(serializers.ModelSerializer):
    class Meta(Check):
        model = Check
        fields = ('id', 'data', 'in_time', 'out_time', 'is_late', 'is_early_left', 'status',)
