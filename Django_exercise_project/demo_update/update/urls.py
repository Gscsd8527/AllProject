from django.urls import path
from update.views import *
app_name = 'update'
urlpatterns = [
    path('update/', update, name='up'),
    path('show/', show, name='show'),
    path('au/', OAuth),
    path('lg/', gitlab_login)
]
