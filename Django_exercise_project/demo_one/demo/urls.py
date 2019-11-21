from django.urls import path
from .views import *
app_name = 'demo'

urlpatterns = [
    path('show', ShowData, name='show'),
]