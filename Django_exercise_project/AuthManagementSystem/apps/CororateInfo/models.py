from django.db import models
from apps.User.models import UserInfo
# Create your models here.

class Information(models.Model):
    """
    员工发布的信息表
    一对多，字段写在多的那边
    """
    user = models.ForeignKey(UserInfo, null=True, blank=True, on_delete=models.CASCADE)
    title = models.TextField(null=False, verbose_name='标题')
    content = models.TextField(null=False, verbose_name='内容')
    publish_time = models.DateTimeField(auto_now_add=True, verbose_name='发布时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')

    class Meta:
        db_table = 'information'
        verbose_name = '公司内部信息表'
        verbose_name_plural = verbose_name
