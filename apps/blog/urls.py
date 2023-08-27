from django.urls import path
from .views import PostViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'',PostViewSet, basename='blog_post')

urlpatterns = [

] + router.urls
