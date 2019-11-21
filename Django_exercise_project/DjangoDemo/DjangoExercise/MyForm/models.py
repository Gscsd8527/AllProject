from django.db import models

# Create your models here.
class MyFormModel(models.Model):
    username = models.CharField(max_length=10, verbose_name='用户名')
    password = models.CharField(max_length=10, verbose_name='密码')
    email = models.EmailField(verbose_name='邮箱')