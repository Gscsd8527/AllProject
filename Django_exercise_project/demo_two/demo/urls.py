from django.urls import path
from .views import *
app_name = 'demo'

urlpatterns = [
    path('show', show, name='show'),
    path('au', OAuth),
]
