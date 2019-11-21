from django.urls import path
from mydemo import views
app_name = 'rest'
urlpatterns = [
    path('show/', views.Show.as_view()),
    path('list/', views.UserListView.as_view()),
    path('filet/', views.UserViewSet.as_view()),
    path('page/', views.Pager1View.as_view()),
]