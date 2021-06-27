"""RestFramework URL Configuration

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
from django.conf.urls import url
from rest_framework.documentation import include_docs_urls


# Java中常用的knife4j的接口文档
from django.conf.urls import url
from rest_framework_swagger.views import get_swagger_view
schema_view = get_swagger_view(title='Java中常用的knife4j的接口文档')


urlpatterns = [
    # url(r'^docs/', include_docs_urls(title='My API title')),  # 自动生成文档 http://127.0.0.1:8000/docs/
    url(r'^docs/$', schema_view),    # 自动生成文档 http://127.0.0.1:8000/docs/
    # path('admin/', admin.site.urls),
    path('Api/', include('Api.urls', namespace='Api')),

]
