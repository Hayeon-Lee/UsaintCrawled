#직접 제작한 파일임

from django.urls import URLPattern, path, include
from .views import crawledData

urlpatterns = [
    path("1/", crawledData),
]
