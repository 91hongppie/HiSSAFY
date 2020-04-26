from rest_framework import serializers
from .models import Campus, Account, Check

class CampusSerializer(serializers.ModelSerializer):
    class Meta(Campus):
        model = Campus
        fields = ('id', 'campus',)


class AccountSerializer(serializers.ModelSerializer):
    class Meta(Account):
        model = Account
        fields = ('id', 'pic_name', 'name', 'stage', 'region', 'classes', 'student_id', 'birthday',)


class CheckSerializer(serializers.ModelSerializer):
    account_check = AccountSerializer(read_only=True)
    
    class Meta(Check):
        model = Check
        fields = ('id', 'date', 'in_time', 'out_time', 'is_late', 'is_early_left', 'status', 'student_info_id', 'account_check',)


# class AccountImageSerializer(serializers.ModelSerializer):
#     class Meta(AccountImage):
#         model = AccountImage
#         fields = ('id', 'pic_name', 'name', 'student_info_id',)


# class FaceSerializer(serializers.ModelSerializer):
#     class Meta(Face):
#         model = Face
#         fields = ('id', 'pic_name', 'top', 'bottom', 'right', 'left', 'account',)
