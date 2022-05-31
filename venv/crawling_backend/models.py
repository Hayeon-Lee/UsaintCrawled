from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

#추후에 클래스 이름 변경
class BoardData(models.Model):
    #첫 페이지에 구할 수 있는 정보들
    studentID = models.IntegerField(null=True, default=0)
    studentGrade = models.IntegerField(null=True, default=0)
    studentSemester = models.IntegerField(null=True, default=0)
    studentEnrolled = models.BooleanField(null=True)

    #학기별 성적조회 페이지에서 구할 수 있는 정보들
    #리스트 왜 안되니~
    #listenList = ArrayField(models.FloatField(max_length=10, blank = True, default=0.0))
    #scoreList = ArrayField(models.FloatField(max_length=10, blank = True, default=0.0))
    graduateScore = models.FloatField(max_length=10, null=True, default=0.0)

    #졸업사정표 페이지에서 구할 수 있는 정보들
    canGraduate = models.BooleanField(null=True)

    grad133_f = models.FloatField(max_length=10, null=True, default=0.0)

    christ4_f = models.IntegerField(null=True, default=0)
    softeng60_f = models.IntegerField(null=True, default=0)
    softbsm18_f = models.IntegerField(null=True, default=0)
    prosoft12_f = models.IntegerField(null=True, default=0)
    archsoft12_f = models.IntegerField(null=True, default=0)

    pyeonip_f = models.BooleanField(null=True)
    gradtest_f = models.BooleanField(null=True)
    elementsci_f = models.BooleanField(null=True)
    allarch_f = models.BooleanField(null=True)
    engarchelem_f = models.BooleanField(null=True)
    matheng_f = models.BooleanField(null=True)
    gradnotice_f = models.BooleanField(null=True)

    libartess_f = models.IntegerField(null=True, default=0)
    libartselect_f = models.IntegerField(null=True, default=0)
    leadership_f = models.IntegerField(null=True, default=0)
    comglobal_f = models.IntegerField(null=True, default=0)
    majorelemsoft_f = models.IntegerField(null=True, default=0)
    majoresssoft_f = models.IntegerField(null=True, default=0)
    majorsoft_f = models.IntegerField(null=True, default=0)

    libertyart_f = models.BooleanField(null=True)
    chaple = models.BooleanField(null=True)
