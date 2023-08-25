from django.urls import path, include
from .views import index, login, logout

urlpatterns = [
    path('', index),
    path('login/', login),
    path('logout/', logout),
    # path('login-data/', login),
]
