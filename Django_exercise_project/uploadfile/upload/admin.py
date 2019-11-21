from django.contrib import admin

# Register your models here.
from upload.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', ]

admin.site.register(Product, ProductAdmin)
