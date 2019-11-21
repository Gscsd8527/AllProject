from django.urls import path
app_name = 'apps.goods'
from apps.goods.views import index
urlpatterns = [
    path('index/', index, name='index')
]