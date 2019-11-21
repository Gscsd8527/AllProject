from django.db import models

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to='img')  # upload_to表示文件会上传到img目录下

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'upload_product'
