from django.urls import path
from .views import auth,  Oauth

app_name = 'Auth'
urlpatterns = [
    # path('(?P<code>[a-zA-Z])()', auth, name='auth'),
    path('auth/', auth, name='auth'),
    path('', Oauth, name='oauth'),
]