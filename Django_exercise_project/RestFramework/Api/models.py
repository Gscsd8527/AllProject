from django.db import models

# Create your models here.


class DataSets(models.Model):
    title = models.TextField(verbose_name='标题')
    body = models.TextField(null=True, verbose_name='主体内容')
    url = models.CharField(max_length=255, null=True, verbose_name='url')
    date = models.CharField(max_length=255, null=True, verbose_name='时间')
    source = models.CharField(max_length=255, null=True, verbose_name='来源')

    class Meta:
        db_table = 'dataset'

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    USER_TYPE = (
        (1, '普通用户'),
        (2, 'VIP'),
        (3, 'SVIP')
    )

    user_type = models.IntegerField(choices=USER_TYPE, default=1)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)

class UserToken(models.Model):
    user = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    token = models.CharField(max_length=64)
