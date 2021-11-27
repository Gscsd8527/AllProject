from django.db import models

# class Permission(models.Model):
#     """
#     权限
#     """
#     title = models.CharField(max_length=32, unique=True, verbose_name=u"权限")
#     url = models.CharField(max_length=128, unique=True)
#     icon = models.CharField(max_length=10, verbose_name=u'权限图标', null=True, blank=True)
#     menu = models.ForeignKey("Menu", null=True, blank=True, on_delete=models.CASCADE)
#
#     def __str__(self):
#         # 显示带菜单前缀的权限
#         return '{menu}---{permission}'.format(menu=self.menu, permission=self.title)
#
#     class Meta:
#         db_table = 'permission'
#         verbose_name = u"权限"
#         verbose_name_plural = verbose_name


class Role(models.Model):
    """
    角色：
        title: 老板、经理、管理层、开发、运维、普通员工等等一些角色，也可叫角色或者权限组
    创建表后手动添加角色和角色id
    """
    title = models.CharField(max_length=32, unique=True, default="普通员工", verbose_name=u"角色")
    title_id = models.IntegerField(max_length=32, default=10, verbose_name=u"代表角色的值")

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'role'
        verbose_name = u"角色"
        verbose_name_plural = verbose_name


class UserInfo(models.Model):
    """
    用户：划分角色
    """
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, unique=True, verbose_name="用户名")  # 用户名设置成唯一值
    password = models.CharField(max_length=64, verbose_name="密码")
    real_name = models.CharField(max_length=50, verbose_name=u"真实姓名", default="")
    email = models.EmailField(max_length=254, unique=True, verbose_name="邮箱")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='删除标记')
    # 多对多，一个人有多个角色，多个人同属于一个角色
    role = models.ManyToManyField(Role)

    class Meta:
        db_table = 'user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

