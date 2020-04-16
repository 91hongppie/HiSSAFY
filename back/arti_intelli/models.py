from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

# Create your models here.
class Campus(models.Model):
    campus = models.CharField(max_length=10)


# 사진, 이름, 생일, 입실시간, 퇴실시간
class Account(models.Model):
    # pic_name = ProcessedImageField(
    #     processors=[ResizeToFit(64, 64)],
    #     format='JPEG',
    #     options={'quality': 100},
    #     upload_to = 'arti_intelli/pic_names',
    #     blank=False,
    # )
    pic_name = models.FileField(upload_to='arti_intelli/pic_names', max_length=100)
    name = models.CharField(max_length=10)
    stage = models.IntegerField()
    classes = models.IntegerField()
    birthday = models.DateField(default='1950-01-01')
    student_id = models.CharField(max_length=7)
    region = models.ForeignKey(Campus, on_delete=models.CASCADE)


class Check(models.Model):
    date = models.DateField(auto_now_add=True)
    in_time = models.TimeField(auto_now=True)
    out_time = models.TimeField(blank=True, null=True)
    is_late = models.BooleanField(default=False)
    is_early_left = models.BooleanField(default=False)
    status = models.IntegerField()
    student_info = models.ForeignKey(Account, on_delete=models.CASCADE)
    
    
class Face(models.Model):
    pic_name = models.FileField(upload_to='arti_intelli/pic_faces', max_length=100)
    top = models.IntegerField()
    bottom = models.IntegerField()
    right = models.IntegerField()
    left = models.IntegerField()
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
