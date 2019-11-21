from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    STATUS_CHOICES = (('draft', 'Draft'), ('published', 'Published'))
    title = models.CharField(max_length=250, verbose_name='文章标题')
    # 通常在URL中使用。slug是一个短的字符串，只能包含字母，数字，下划线和减号。将使用slug字段构成优美的URL，也方便搜索引擎搜索
    # unique_for_date参数表示不允许两条记录的publish字段日期和title字段全都相同，这样就可以使用文章发布的日期与slug字段共同生成一个唯一的URL标识该文章。
    slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name='url')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='作者')
    body = models.TextField()
    # 自带datetime.now()
    publish = models.DateTimeField(default=timezone.now(), verbose_name='时间')
    # auto_now_add表示当创建一行数据的时候，自动用创建数据的时间填充
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # auto_now表示每次更新数据的时候，都会用当前的时间填充该字段
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    # choices参数，所以这个字段的值只能为一系列选项中的值。
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    class Meta:
        # 指定了Django在进行数据库查询的时候，默认按照发布时间的逆序将查询结果排序。
        # 逆序通过加在字段名前的减号表示。这样最近发布的文章就会排在前边。
        ordering = ('-publish',)

    # __str__()方法是Python类的功能，供显示给人阅读的信息，这里将其设置为文章的标题。
    # Django在很多地方比如管理后台中都调用该方法显示对象信息。
    def __str__(self):
        return self.title