from django.contrib import admin
from MyForm.models import MyFormModel
# Register your models here.

class MyFormAdmin(admin.ModelAdmin):
    list_display = ['username', 'password', 'email']

admin.site.register(MyFormModel, MyFormAdmin)