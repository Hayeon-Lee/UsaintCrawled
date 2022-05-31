from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
# Create your views here.

from .models import BoardData
from .serializers import BoardDataSerializer

@api_view(['GET'])
def crawledData(request):
    totalData = BoardData.objects.filter(studentID__startswith = '20201759')
    #사용자 ID인 것만 검색해서 갖고오게 해야함

    serializer = BoardDataSerializer(totalData, many = True)
    #many=true , 다량의 데이터를 직렬화 해줌
    return Response(serializer.data)