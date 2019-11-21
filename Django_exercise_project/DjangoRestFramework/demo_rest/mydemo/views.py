from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializers
from django.http import HttpResponse
import json
from rest_framework import status
# Create your views here.
from .models import User

from rest_framework import mixins
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework import viewsets

class Show(APIView):
    def get(self, request, format=None):
        # 序列化数据方式1
        # users = User.objects.all()
        # print(users.values_list())
        # serializer = UserSerializers(instance=users, many=True)
        # users_ret = json.dumps(serializer.data, ensure_ascii=False)
        # # return Response(users_ret)
        # return HttpResponse(users_ret)

        # 序列化方式2
        users = User.objects.all()
        serializer = UserSerializers(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        接收前端闯过来的数据并保存起来，
        :return:
        """
        serilizer = UserSerializers(data=request.data)
        if serilizer.is_valid():
            # 会去调用create方法
            serilizer.save()
            return Response(serilizer.data, status=status.HTTP_201_CREATED)
        return Response(serilizer.data, status=status.HTTP_400_BAD_REQUEST)


# class UserListView(mixins.ListModelMixin, generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializers
    # def get(self, request, *arg, **kwargs):
    #     return self.list(request, *arg, **kwargs)

# 自定义分页
class UserPageView(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = UserPageView

# 介绍viewset
# class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
#     pass


# 过滤
# class UserViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
class UserViewSet(APIView):
    # queryset = User.objects.all()
    serializer_class = UserSerializers
    pagination_class = UserPageView
    def get_queryset(self):
        return User.objects.filter(age__lt=30)



# 分页2 主要依赖setting中的配置
# http://127.0.0.1:8000/rest/page/?page=1 自己填page
class Pager1View(APIView):
    def get(self,request,*args,**kwargs):
        #获取所有数据
        roles = User.objects.all()
        #创建分页对象
        pg = PageNumberPagination()
        #获取分页的数据
        page_roles = pg.paginate_queryset(queryset=roles,request=request,view=self)
        #对数据进行序列化
        ser = UserSerializers(instance=page_roles,many=True)
        return Response(ser.data)