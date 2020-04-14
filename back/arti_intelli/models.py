from django.db import models
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

# Create your models here.
class Campus(models.Model):
    campus = models.CharField(max_length=10)


# 사진, 이름, 생일, 입실시간, 퇴실시간
class Account(models.Model):
    pic_name = ProcessedImageField(
        processors=[ResizeToFit(64, 64)],
        format='JPEG',
        options={'quality': 100},
        upload_to = 'arti_intelli/pic_names/',
        blank=False,
    )
    name = models.CharField(max_length=10)
    stage = models.IntegerField()
    classes = models.IntegerField()
    birthday = models.DateField(default='1950-01-01')
    student_id = models.CharField(max_length=7)
    region = models.ForeignKey(Campus, on_delete=models.CASCADE)


class Check(models.Model):
    date = models.DateField(auto_now_add=True)
    in_time = models.DateTimeField(auto_now_add=True)
    out_time = models.DateTimeField(blank=True, null=True)
    is_late = models.BooleanField(default=False)
    is_early_left = models.BooleanField(default=False)
    status = models.IntegerField()
    student_info = models.ForeignKey(Account, on_delete=models.CASCADE)
