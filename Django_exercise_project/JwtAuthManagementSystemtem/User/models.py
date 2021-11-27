from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    real_name = models.CharField(max_length=50, verbose_name="真实姓名", default="")
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name
