from django.urls import path
app_name = 'upload'
from upload.views import *
urlpatterns = [
    path('upload/', Upload, name='up'),
    path('show/', show, name='show')
]
