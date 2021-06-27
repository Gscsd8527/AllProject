from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from Api.models import DataSets, UserInfo, UserToken
from .serializers import DataSetsSerializers
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
import jwt
from rest_framework_simplejwt import authentication
from Api.auth import JewQueryParamsAuthenticate
from .permission import *
import datetime
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate
from Api.utils.jwt_auth import create_token
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class QuerySet(APIView):
    """
    数据集
    """
    def get(self, request, format=None):
        try:
            # 获取 get 请求中的 json字符串参数
            data = request.query_params
            print(data)
            print(data.get('A'))  # 获取当前键的值
            resp = {
                'code': 200,
                'message': 'success',
            }
        except Exception as e:
            resp = {
                'code': 300,
                'message': str(e),
            }
        return Response(resp)

    def post(self, request):
        # 获取 post 请求参数
        print(request.data)
        return HttpResponse('post')


class DataSetsListAPIView(APIView):
    def get(self, request):
        # 查询所有的书籍
        dataset = DataSets.objects.all()
        # 将对象列表转换成字典列表
        serializer = DataSetsSerializers(instance=dataset, many=True)
        # 返回响应
        return Response(serializer.data)

    def post(self, request):
        # 获取参数
        data_dict = request.data
        print('data_dict = ', data_dict)
        # 创建序列化器
        serializer = DataSetsSerializers(data=data_dict)
        # 校验:
        """
        is_valid 这个效验的作用是将 post 发送过来的进行效验，看看是否符合 serializer 文件中定义的规则
        最常比较的就是格式是否一致，其次还能判断字段的数值之类的，比如 性别字段，只能有男女，年龄必须大于0岁
        也可： 判断传进来的数值是否已经在库中
        列:
        class DataSetsSerializers(serializers.ModelSerializer):
            class Meta:
                model = DataSets
                fields = "__all__"
            
            attrs 是 post 中传过来的参数，这个字段得是model中定义过的,因为前面的序列化时候把非序列化文件中的字段都过滤掉了
            def validate(self, attrs):
                readcount = attrs['readcount']
                commentcount = attrs['commentcount']
                if commentcount > readcount:
                    raise serializers.ValidationError('评论量不能大于阅读量')  # 这个值里面可以弄成 json类型，前端好接收
                return attrs
        """
        serializer.is_valid(raise_exception=True)
        # 入库
        serializer.save()
        # 返回响应
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# 使用二级视图GenericAPIView实现列表视图
class BookListGenericAPIView(GenericAPIView):
    # 提供公共的属性
    queryset = DataSets.objects.all()
    serializer_class = DataSetsSerializers

    def get(self, request):
        # 查询所有的书籍(2种)
        # books = self.queryset
        books = self.get_queryset()
        # print(books)
        # 将对象列表转换成字典列表(3种方法)
        # serializer = self.serializer_class(instance=books, many=True)
        # serializer = self.get_serializer_class()(instance=books, many=True)
        serializer = self.get_serializer(instance=books, many=True)

        # 弄成翻页形式
        # pg = PageNumberPagination()
        # page_roles = pg.paginate_queryset(queryset=books, request=request, view=self)
        # serializer = DataSetsSerializers(instance=page_roles, many=True)

        # 返回响应
        return Response(serializer.data)

    def post(self, request):
        # 获取参数
        data_dict = request.data
        # 创建序列化器
        serializer = self.get_serializer(data=data_dict)
        # 校验
        serializer.is_valid(raise_exception=True)
        # 入库
        serializer.save()
        # 返回响应
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#Mixin和二级视图GenericAPIView,实现列表视图
class BookListMixinGenericAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    # 提供公共的属性
    queryset = DataSets.objects.all()
    serializer_class = DataSetsSerializers

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)



# 使用viewset实现获取所有和单个
# path('viewset/', views.BooksViewSet.as_view({'get': 'list'})),
# path('viewset/<pk>/', views.BooksViewSet.as_view({'get': 'retrieve'})),
class BooksViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving books.
    """
    def list(self, request):
        queryset = DataSets.objects.all()
        serializer = DataSetsSerializers(instance=queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = DataSets.objects.all()
        book = get_object_or_404(queryset, pk=pk)
        serializer = DataSetsSerializers(instance=book)
        return Response(serializer.data)


# http://127.0.0.1:8000/show5/
# get 获取所有   post: 新增
class BookListThirdView(ListAPIView, CreateAPIView):
    # 提供公共的属性
    queryset = DataSets.objects.all()
    serializer_class = DataSetsSerializers


class ModelViewSet(viewsets.ModelViewSet):
    queryset = DataSets.objects.all()
    serializer_class = DataSetsSerializers

    # pagination_class = PageNum
    # 限流自定义
    # throttle_classes = [UserRateThrottle]
    # 指定过滤方法
    # filter_backends = (DjangoFilterBackend,OrderingFilter)
    # ordering_fields=('data_joined','id')
    # filter_fields=('username','phone','is_active')
    def get_serializer_class(self):
        return DataSetsSerializers


class AuthenticationViewSet(ListAPIView, CreateAPIView):
    # 局部认证
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = [AllowAny]

    # 提供公共的属性
    queryset = DataSets.objects.all()
    serializer_class = DataSetsSerializers


def md5(user):
    import hashlib
    import time

    # 当前时间，相当于生成一个随机的字符串
    ctime = str(time.time())

    # token加密
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()


class AuthView(APIView):
    """
    用于用户登录验证
    """
    authentication_classes = []      #里面为空，代表不需要认证
    permission_classes = []          #里面为空，代表不需要权限

    def post(self, request, *args,**kwargs):
        ret = {'code': 200, 'msg': None}
        try:
            user = request.POST.get('username')
            pwd = request.POST.get('password')
            print(user, pwd)
            obj = UserInfo.objects.filter(username=user, password=pwd).first()
            print(obj.username, obj.password)
            if not obj:
                ret['code'] = 300
                ret['msg'] = '用户名或密码错误'
            #为用户创建token
            token = md5(user)
            #存在就更新，不存在就创建
            UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            ret['token'] = token
        except Exception as e:
            ret['code'] = 300
            ret['msg'] = '请求异常'
        return Response(ret)


ORDER_DICT = {
    1:{
        'name':'apple',
        'price':15
    },
    2:{
        'name':'狗子',
        'price':100
    }
}


# http://127.0.0.1:8000/order/?token=c14f6fff73ec5220a68cce464004bee8
class OrderView(APIView):
    # 用户想要获取订单，就要先通过身份认证、在全局settings.py 中已经配置
    # permission_classes = [SVIPPremission, ]

    def get(self, request, format=None):
        try:
            print(request.user)
            # print(request.auth)
            resp = {
                'code': 200,
                'msg': '订单获取成功',
            }
        except Exception as e:
            resp = {
                'code': 300,
                'msg': str(e),
            }
        return Response(resp)


class UserInfoView(APIView):
    # permission_classes = [SVIPPremission, ]
    def get(self, request, *args, **kwargs):
        return HttpResponse('SVIP用户信息')


# 生成token
class JwtTokenView(APIView):
    def get(self, request, *args, **kwargs):
        username = '小橙子'
        password = 'i love you'
        # user_object = UserInfo.objects.filter(username=username, password=password).first()
        user_object, created = UserInfo.objects.update_or_create(username=username, password=password)
        print(user_object, created)
        if not user_object:
            return Response({'code': 300, 'message': '用户名或密码错误'})
        token = create_token({'user_type': user_object.user_type, 'username': user_object.username})
        return Response({'code': 200, 'token': token})


# 验证token
class JwtCheckTokenView(APIView):
    authentication_classes = [JewQueryParamsAuthenticate, ]
    def get(self, request, *args, **kwargs):
        try:
            print('------------', request.user)
            resp = {
                'code': 200,
                'message': 'success',
                'data': request.user
            }
        except Exception as e:
            resp = {
                'code': 300,
                'message': str(e)
            }
        return Response(resp)


# 过滤
# http://127.0.0.1:8000/dataset/
# 分别通过title 和 date 去查询
# http://127.0.0.1:8000/dataset/?title=英研制神奇胶囊自行车：时速可达145公里
# http://127.0.0.1:8000/dataset/?date=2014-05-23
class FilterView(ModelViewSet):
    queryset = DataSets.objects.all()

    # 过滤器 和 过滤字段
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('title', 'date')


# 排序
# 分别通过date和id 排序
# http://127.0.0.1:8000/ordering/?ordering=-date
# http://127.0.0.1:8000/ordering/?ordering=id
class OrderingView(ModelViewSet):
    queryset = DataSets.objects.all()

    # 排序器 和 排序字段
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_fields = ('title', 'id', 'date')
