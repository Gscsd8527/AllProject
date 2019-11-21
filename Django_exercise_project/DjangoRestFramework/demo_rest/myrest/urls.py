from django.urls import path
from myrest import views
app_name = 'myrest'
urlpatterns = [
    path('test/', views.Test.as_view())
]