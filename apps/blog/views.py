from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.viewsets import ModelViewSet 
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings
from config.middlewares import cache_page_after_callback
from .models.models import Post
from .serializers import PostSerializer
from .tasks import increment_post_view
from .services import BlogService 
from django.views.decorators.cache import cache_page


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @method_decorator(
    cache_page_after_callback(
    CACHE_TTL,
    callbacks=[lambda request:increment_post_view.delay(BlogService.get_request_kwargs(request)['pk'])]
    ),
    name='cached_retrieve'
    )
    def retrieve(self, *args, **kwargs):
        ID = BlogService.get_request_kwargs(self.request)['pk']
        increment_post_view.delay(ID)
        serializer_class = self.get_serializer_class()
        post_queryset = self.get_queryset().filter(id=ID)
        post_data = serializer_class(*post_queryset).data
        return Response(post_data)
  