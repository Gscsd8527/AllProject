from django.db import models
from django.contrib.auth.models import AbstractUser
from db.base_model import BaseModel
# Create your models here.
# class User(models.Model):
#     name = models.CharField(max_length=30, verbose_name='姓名')
#     sex = models.CharField(max_length=10, choices=(('0', '女'), ('1', '男')), verbose_name='员工性别')
#     age = models.IntegerField(verbose_name='年龄')
#     addr = models.TextField(verbose_name='家庭地址')
#     on_delete = models.BooleanField(default=False, verbose_name='是否已删除')
#
#     class Meta:
#         db_table = 'xadmin_user'
#
#     def __str__(self):
#         return self.name

# class User(AbstractUser, BaseModel):
#     class Meta:
#         db_table = 'df_user'
#         verbose_name = '用户'
#         verbose_name_plural = verbose_name

class User(AbstractUser):
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name