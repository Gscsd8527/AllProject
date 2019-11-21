from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from mydemo.models import User
import json
# Create your views here.

class Test(View):
    """注册"""
    def get(self, request):
        # 显示注册页面
        data = User.objects.all()
# 1.  这种方式返回结果数据
#         json_list = []
#         for dt in data:
#             json_dict = {}
#             json_dict['name'] = dt.name
#             json_dict['sex'] = dt.sex
#             json_dict['age'] = dt.age
#             json_dict['addr'] = dt.addr
#             json_list.append(json_dict)
#         # 这样返回的是列表格式
#         # return HttpResponse(json_list)
#         # 这样返回的是json格式，而且要加上content_type="application/json"
#         return HttpResponse(json.dumps(json_list), content_type="application/json")

# 2. 也可使用这种
#         json_list = []
#         from django.forms.models import model_to_dict
#         for dt in data:
#             json_dict = model_to_dict(dt)
#             json_list.append(json_dict)
#         return HttpResponse(json.dumps(json_list), content_type="application/json")

# 3. 也可使用这种
#         from django.core import serializers
#         json_data = serializers.serialize("json", data)
#         json_data = json.loads(json_data)
#         return HttpResponse(json.dumps(json_data), content_type="application/json")

# 4. 也可以用这种方法
        from django.http import JsonResponse
        from django.core import serializers
        json_data = serializers.serialize("json", data)
        json_data = json.loads(json_data)
        return JsonResponse(json_data, safe=False)


