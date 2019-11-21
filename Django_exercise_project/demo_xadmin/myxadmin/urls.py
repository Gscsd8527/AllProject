from django.urls import path
from .views import Index
app_name = 'myxadmin'
urlpatterns = [
    path('index/', Index),
]