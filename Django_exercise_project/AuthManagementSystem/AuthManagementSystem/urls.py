"""AuthManagementSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# knife4j的接口文档
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='knife4j的接口文档')

# rest_framework 自带的接口文档
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^docs/$', schema_view, name='docs'),  # 自动生成文档：如果我们视图里面有 权限限制的话，会报错。认证能通过，权限效验过不去，使用的时候要将有权限校验的路径注销掉
    url(r'^docs/', include_docs_urls(title='Django RestFramework 文档')),  # 这个文档不受限制，但是这个文档不好用
    path('user/', include('User.urls', namespace='user')),
    path('info/', include('CororateInfo.urls', namespace='user')),
]
