from django.urls import path, include
from .views import delay_view


urlpatterns = [
    path('', delay_view),

]
