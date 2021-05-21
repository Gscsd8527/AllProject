from django.urls import path
from Api import views
from rest_framework.routers import SimpleRouter,DefaultRouter
app_name = 'Api'

routed=DefaultRouter()
routed.register(r'show4', views.ModelViewSet)

urlpatterns = [
    path('show/', views.QuerySet.as_view()),
    path('show1/', views.DataSetsListAPIView.as_view()),
    path('show2/', views.BookListGenericAPIView.as_view()),

    path('show3/', views.BookListMixinGenericAPIView.as_view()),

    path('show5/', views.BookListThirdView.as_view()),

    path('show6/', views.AuthenticationViewSet.as_view()),

    path('viewset/', views.BooksViewSet.as_view({'get': 'list'})),
    path('viewset/<pk>/', views.BooksViewSet.as_view({'get': 'retrieve'})),


    path('auth/', views.AuthView.as_view()),
    path('order/', views.OrderView.as_view()),
    path('userinfo/', views.UserInfoView.as_view()),


    # path('show4/', views.ModelViewSet.as_view()),

    path('jwt/', views.JwtTokenView.as_view()),
    path('testjwt/', views.JwtCheckTokenView.as_view()),
]
urlpatterns+=routed.urls