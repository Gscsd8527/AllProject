from django.contrib import admin
from AutoCert.models import UserInfo, UserToken
# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user_type', 'username', 'password']

admin.site.register(UserInfo, UserInfoAdmin)