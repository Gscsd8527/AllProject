from django.urls import path
from django.conf.urls import url
from apps.user.views import RegisterView, ActiveView, LoginView
app_name = 'apps.user'

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='register'),  # 注册页面
    url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'), # 用户激活
    url(r'login/$', LoginView.as_view(), name='login') # 登录

]
