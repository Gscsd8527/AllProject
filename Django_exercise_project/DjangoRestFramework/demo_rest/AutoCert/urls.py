from django.urls import path
from AutoCert import views
app_name = 'auto'
urlpatterns = [
    path('auth/', views.AuthView.as_view()),
    path('user/', views.UserInfoView.as_view())
]