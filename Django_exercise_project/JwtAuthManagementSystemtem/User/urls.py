from django.urls import path
from User import views
from rest_framework_jwt.views import obtain_jwt_token
app_name = 'user'


urlpatterns = [
    path('register/', views.UserRegisterView.as_view()),
    path('login/', views.UserLogingView.as_view()),
    path('jwt-login/', obtain_jwt_token),  # 会返回一个token,如果在setting中JWT_RESPONSE_PAYLOAD_HANDLER自定义了返回格式之后，会按照我们要求的格式返回
    path('info/', views.UserInfoView.as_view()),
]
