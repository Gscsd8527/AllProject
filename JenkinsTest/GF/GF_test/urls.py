from django.urls import path
from GF_test import views

app_name = 'GF'

urlpatterns = [
    # query1对应下拉框，前五个模糊搜索
    path('query1/<str:keyword>', views.keyword),
    # query2对应检索，得到泡泡集合
    path('query2/<str:keyword>', views.keyword_query),
    # query3对应点击泡泡，得到检索值和泡泡值，返回图谱
    path('query3/<str:keyword>,<str:keyword_pao>', views.pao_query),

]
