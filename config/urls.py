"""config URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('api/v1/api-docs/', include_docs_urls(title='Elm-o-SanatBlog API')),
    path('api/v1/schema', get_schema_view(
            title="Your Project",
            description="API for all things …",
            version="1.0.0"
        ),
        name='openapi-schema'),
    path('blog/', include('apps.blog.urls')),
    path('', include('apps.authentication.urls')),
    # path('api/v1/blog/', include('apps.blog.urls')),
    path('api/v1/delay/', include('apps.delay.urls')),
    
    # path('v1/auth/', include('apps.auth.urls')),
]
