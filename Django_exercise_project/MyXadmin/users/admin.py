# from django.contrib import admin
# from users.models import UserInfo
# from xadmin import views
# import xadmin
#
# # Register your models here.
# class UserAdmin(object):
#     list_display = ['id', 'username', 'alias','gender', 'email', 'mobile', 'dept_id', 'is_active', 'is_superuser']
#     # list_filter = ('username')
#     # search_fields = ('username')
#
# xadmin.site.unregister(UserInfo)
# xadmin.site.register(UserInfo, UserAdmin)
#
# # 会在右上角导航栏那多一个主题
# class BaseSetting(object):
#     enable_themes = True
#     use_bootswatch = True
# xadmin.site.register(views.BaseAdminView, BaseSetting)
#
# class GlobalSetting(object):
#     site_title = "后台管理系统"
#     site_footer = "https://www.csdn.net/"
# xadmin.site.register(views.CommAdminView, GlobalSetting)