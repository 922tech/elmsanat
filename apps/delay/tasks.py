from celery import shared_task
import time
from django.shortcuts import redirect
from django.http import HttpResponse

@shared_task
def answer_late():
    time.sleep(5)
    return redirect("https://www.google.com")
