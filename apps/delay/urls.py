from django.urls import path, re_path, include
from .views import  stream

urlpatterns = [
    path('stream',stream)

]
