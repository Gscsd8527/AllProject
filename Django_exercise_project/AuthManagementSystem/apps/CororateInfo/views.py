from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from apps.User.models import UserInfo
from .serializers import InformationSerializers
from .models import Information
from Utils.auth import JewQueryParamsAuthenticate
from Utils.utils import resp_success_status, resp_error_status


class PublishInfoView(APIView):
    """
    发布信息
    """
    authentication_classes = (JewQueryParamsAuthenticate,)  # 需要验证当前用户信息

    def post(self, request, format=None):
        user_id = request.user['user_id']  # request.user 中包含了我们放入创建token是放入的值，这个值
        user = UserInfo.objects.filter(id=user_id).first()
        title = request.POST.get('title')
        content = request.POST.get('content')
        if all([title, content]):
            Information.objects.create(user=user, title=title, content=content)
            resp = resp_success_status(msg="发布成功")
        else:
            resp = resp_error_status(msg="标题和文本内容有空值")
        return Response(resp)


class InfoView(viewsets.ViewSet):
    """
    获取信息:
       未登录状态，查看所有和查看单个数据
    """
    def list(self, request):
        queryset = Information.objects.filter(is_delete=False)
        serializer = InformationSerializers(instance=queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Information.objects.filter(is_delete=False)
        info = get_object_or_404(queryset, pk=pk)
        serializer = InformationSerializers(instance=info)
        return Response(serializer.data)
