from django.db import models

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=30, verbose_name='姓名')
    sex = models.CharField(max_length=10, choices=(('0', '女'), ('1', '男')), verbose_name='员工性别')
    age = models.IntegerField(verbose_name='年龄')
    addr = models.TextField(verbose_name='家庭地址')
    on_delete = models.BooleanField(default=False, verbose_name='是否已删除')

    class Meta:
        db_table = 'user'

    def __str__(self):
        return self.name
