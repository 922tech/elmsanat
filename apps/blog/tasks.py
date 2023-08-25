from celery import shared_task
from django.db.models import F, QuerySet
from .models.models import Post
import time

@shared_task
def increment_post_view(post_obj: QuerySet):
    time.sleep(10)

    if not isinstance(post_obj, int):
        post_obj = Post.objects.filter(id=post_obj)

    post_obj.update(views=F("views") + 1)
    
    print('\n***************\nTASK DONE\n*****************')


 