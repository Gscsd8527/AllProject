# Generated by Django 2.1.4 on 2019-04-12 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('sex', models.CharField(choices=[('0', '女'), ('1', '男')], max_length=10, verbose_name='员工性别')),
                ('age', models.IntegerField(verbose_name='年龄')),
                ('addr', models.TextField(verbose_name='家庭地址')),
                ('on_delete', models.BooleanField(default=False, verbose_name='是否已删除')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
