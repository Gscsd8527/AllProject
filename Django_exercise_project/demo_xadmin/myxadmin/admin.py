from django.contrib import admin
from myxadmin.models import User
from xadmin import views
import xadmin
# Register your models here.

class UserAdmin():
    list_display = ['id', 'username', 'email', 'last_name']
    list_filter = ['username']
    search_fields = ['username']

xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)

from xadmin import views

# 会在右上角导航栏那多一个主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSetting(object):
    site_title = "后台管理系统"
    site_footer = "https://www.csdn.net/"
xadmin.site.register(views.CommAdminView, GlobalSetting)

