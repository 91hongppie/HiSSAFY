from django.contrib import admin
from .models import Campus, Account, Check, AccountImage

# Register your models here.
class CampusAdmin(admin.ModelAdmin):
    list_display = ('id', 'campus',)
admin.site.register(Campus, CampusAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'pic_name', 'name', 'stage', 'classes', 'birthday', 'region',)
admin.site.register(Account, AccountAdmin)


class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'in_time', 'out_time', 'is_late', 'is_early_left', 'status', 'student_info_id',)
admin.site.register(Check, CheckAdmin)


class AccountImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'pic_name', 'name', 'student_info_id',)
admin.site.register(AccountImage, AccountImageAdmin)


# class FaceAdmin(admin.ModelAdmin):
#     list_display = ('id', 'pic_name', 'top', 'bottom', 'right', 'left', 'account_id')
# admin.site.register(Face, FaceAdmin)
