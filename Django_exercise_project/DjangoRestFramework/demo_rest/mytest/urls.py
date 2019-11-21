from django.urls import path
app_name = 'test'
from mytest.views import *
urlpatterns = [
    path('test/<int:id>', test, name='test'),
    path('mytest/', mytest, name='mytest'),
    path('api/', api_root, name='api'),
]