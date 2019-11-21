from django.urls import path
app_name = 'MyForm'

from MyForm.views import Login, loginForm, register
urlpatterns = [
    path('login/', Login, name= 'login'),
    path('form/', loginForm, name= 'login_form'),
    path('register/', register, name= 'register')
]