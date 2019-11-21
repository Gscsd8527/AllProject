from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
# Create your views here.
@api_view(['GET', 'POST'])
def test(request, id):
    if request.method == 'GET':
        return Response('hello' + str(id))

@api_view(['GET', 'POST'])
def mytest(request, format=None):
    resp = {
        'code': 100,
        'msg': 'hello'
    }
    return Response(resp)

@api_view(['GET', 'POST'])
def api_root(request, format=None):
    """
     分别对应下放的两个返回，不加request和format只能返回相对路径
       {
        "users": "http://127.0.0.1:8000/test/mytest/",
        "aa": "/test/mytest/"
    }
    """
    return Response({
        'users': reverse('test:mytest', request=request, format=format),
        'aa': reverse('test:mytest'),
        # 'snippets': reverse('/test/test/', request=request, format=format)
    })

