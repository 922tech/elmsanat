from typing import Any, Callable, Optional
from django.middleware.cache import CacheMiddleware
from django.utils.decorators import decorator_from_middleware_with_args
from typing import Callable, Any, Sequence
from django.http import HttpResponse


class CacheCallbackMiddleware(CacheMiddleware):
    """
    A cache middleware class that has a `callbackes` attribute.
    callbackes is a sequence that contains callback functions 
    which will be called before fetching the data from cache
    """
    callbacks = []

    @classmethod
    def set_callback_funcs(cls, callbacks):
        cls.callbacks = callbacks
        return cls

    def call_callbacks(self, request) -> None:
        for function in self.callbacks:
            function(request)

    def process_request(self, request): # from fetch
        self.call_callbacks(request)
        return super().process_request(request)
        

def cache_page_after_callback(
    timeout, 
    *, 
    cache=None, 
    key_prefix=None, 
    callbacks: Sequence[Callable[[HttpResponse],Any]]
    ) -> Callable[[Callable[[Any],Any]], Callable]:
    """
    Works like cache_page but also sets callback functions 
    to the cache middleware class
    """
    middleware_class = CacheCallbackMiddleware.set_callback_funcs(callbacks)

    return decorator_from_middleware_with_args(middleware_class)(
    page_timeout=timeout,
    cache_alias=cache,
    key_prefix=key_prefix,
)
