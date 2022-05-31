from rest_framework import serializers
from .models import BoardData

class BoardDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardData
        fields = (
            'studentID','studentGrade', 'studentSemester', 'studentEnrolled'
            , 'graduateScore'
            , 'canGraduate'
            , 'grad133_f'
            , 'christ4_f', 'softeng60_f', 'softbsm18_f', 'prosoft12_f', 'archsoft12_f'
            , 'pyeonip_f', 'gradtest_f', 'elementsci_f', 'allarch_f', 'engarchelem_f', 'matheng_f', 'gradnotice_f'
            ,  'libartess_f', 'libartselect_f', 'leadership_f', 'comglobal_f', 'majorelemsoft_f', 'majoresssoft_f', 'majorsoft_f'
            , 'libertyart_f', 'chaple'
        )