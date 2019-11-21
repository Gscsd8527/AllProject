from django.urls import path, include
app_name = 'myRest'
from .views import Index
urlpatterns = [
    path('', Index, name='index')
]