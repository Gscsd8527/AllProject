from django.urls import path
from apps.CororateInfo import views

app_name = 'users'

urlpatterns = [
    path('publish/', views.PublishInfoView.as_view()),
    path('infoview/', views.InfoView.as_view({'get': 'list'})),
    path('infoview/<pk>', views.InfoView.as_view({'get': 'retrieve'})),
]
