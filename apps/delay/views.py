from django.shortcuts import render
from django.http import HttpResponse
from .tasks import answer_late

def delay_view(request):
    c = answer_late.delay()
    print('status  ',c.status)
    print('success  ',c.successful())
    return HttpResponse('<h3>You will be redirected to google.com in about 5 seconds!</h3>')
# Create your views here.
