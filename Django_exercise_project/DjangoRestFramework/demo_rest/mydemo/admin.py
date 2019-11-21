from django.contrib import admin
from .models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'sex', 'age', 'addr']

admin.site.register(User, UserAdmin)
