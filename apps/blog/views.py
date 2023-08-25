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
# from time import time
# from django.core.cache import cache


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

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
    
    # # def get_decorated(self, *args, **kwargs):
    # #     return R(self, *args, **kwargs)
    
    # def retrieve(self, *args, **kwargs):
    #     ID = self.request.parser_context['kwargs'].get('pk')
    #     increment_post_view.delay(ID)
    #     t1 = time()
    #     R = method_decorator(cache_page(CACHE_TTL), name='cached_retrieve')(self.Retrieve)
    #     t2 = time()
    #     print(t2-t1)
    #     return R(self, *args, **kwargs)

    # @method_decorator(cache_page(CACHE_TTL))
    # def retrieve(self, *args, **kwargs):
        # print('**************  ',(self.request.user),'  **************')

        # t0 = time()
        # ID = self.request.parser_context['kwargs'].get('pk')

        # post = cache.get('post__id__{}'.format(ID))
        # increment_post_view.apply_async(args=[ID])
        # t1 = time()
        # # increment_post_view.delay(ID)
        # # increment_post_view(ID)
        # print('**************  ',t1-t0,'  **************')

        # if post:
        #     return Response(post)
        
        # else:
        #     t2 = time()
            
        #     post_queryset = self.get_queryset().filter(id=ID)
        #     # t3 = time()
        #     if list(post_queryset) is None:
        #         return Response({'response':'object not found'}, status=404)
        #     t3 = time()
        #     serializer_class = self.get_serializer_class()
        #     post_data = serializer_class(*post_queryset).data
        #     t4 = time()
        #     cache.set('post__id__{}'.format(ID), post_data)
        #     t5 = time()
        
        #     increment_post_view.delay(post_queryset)
        #     t6 = time()
        #     print('\n**************  ',t1-t0, t2-t1, t3-t2, t4-t3, t5-t4, t6-t5,'  **************\n')
        #     return Response(post_data)
    
    