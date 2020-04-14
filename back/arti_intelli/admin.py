from django.contrib import admin
from .models import Campus, Account, Check

# Register your models here.
class CampusAdmin(admin.ModelAdmin):
    list_display = ('campus',)
admin.site.register(Campus, CampusAdmin)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'pic_name', 'name', 'stage', 'classes', 'birthday', 'region',)
admin.site.register(Account, AccountAdmin)


class CheckAdmin(admin.ModelAdmin):
    list_display = ('id', 'date', 'in_time', 'out_time', 'is_late', 'is_early_left', 'status')
admin.site.register(Check, CheckAdmin)
