
from django.db import models



class User(models.Model):
    """
    用户表
    """
    username = models.CharField(max_length=20, verbose_name=u'用户名')
    password = models.CharField(max_length=20, verbose_name=u'用户密码')
    time = models.DateTimeField(auto_now_add=True, verbose_name=u'注册时间')

    def __str__(self):
        return self.username


class File(models.Model):
    """
    文件
    """
    filename = models.CharField(max_length=128, verbose_name=u'文件名')
    owner = models.ForeignKey(User, verbose_name=u'所属用户')
    size = models.IntegerField(verbose_name=u'文件大小')
    status = models.IntegerField(verbose_name=u'完成状态')
    path = models.CharField(max_length=64, verbose_name=u'文件路径')
    md5 = models.CharField(max_length=64, verbose_name=u'md5码')
    upload = models.DateTimeField(auto_now_add=True, verbose_name=u'上传时间')

    def __str__(self):
        return self.filename
