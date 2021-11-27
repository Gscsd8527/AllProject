from django.urls import path
from apps.User import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', views.UserLogingView.as_view()),
    path('userinfo/', views.UserInfoView.as_view()),
    path('update/', views.UserInfoUpdateView.as_view()),
    path('delete/', views.UserDeleteView.as_view()),
]
