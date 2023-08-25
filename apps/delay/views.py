from django.shortcuts import render
from django.http import HttpResponse
from .tasks import answer_late

def delay_view(request):
    c = answer_late.delay()
    print('status  ',c.status)
    print('success  ',c.successful())
# Create your views here.
