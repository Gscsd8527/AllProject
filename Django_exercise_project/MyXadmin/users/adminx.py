from xadmin import views
import xadmin

from .models import MyUserInfo, EmailVerifyRecord

# Register your models here.
# class UserAdmin(object):
#     list_display = ['id', 'username', 'alias','gender', 'email', 'mobile', 'dept_id', 'is_active', 'is_superuser']
#     # list_filter = ('username')
    # search_fields = ('username')

# xadmin.site.unregister(UserInfo)
# xadmin.site.register(UserInfo, UserAdmin)
#
class MyUserInfoAdmin(object):
    # pass
    list_display = ['id', 'username', 'email', 'is_active', 'is_superuser']
    # search_fields = ['username', 'email', 'is_active', 'is_superuser']
    # list_filter = [ 'username', 'email', 'is_active', 'is_superuser']
xadmin.site.register(MyUserInfo, MyUserInfoAdmin)
# xadmin.site.unregister(MyUserInfo)

class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_time']

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


# 会在右上角导航栏那多一个主题
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True
xadmin.site.register(views.BaseAdminView, BaseSetting)

class GlobalSetting(object):
    site_title = "后台管理系统"
    site_footer = "https://www.csdn.net/"
xadmin.site.register(views.CommAdminView, GlobalSetting)

