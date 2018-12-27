from django.db import models
from blog.models import UserInfo
# Create your models here.

# 用户表
class User(models.Model):
    user_info = models.OneToOneField(verbose_name="用户名",to=UserInfo,on_delete=models.CASCADE)
    role = models.ManyToManyField(to='Role')

    def __str__(self):
        return self.user_info


# 角色表
class Role(models.Model):
    STATUS_CHOICES = (
        (0,"无效"),
        (1,"有效")
    )
    name = models.CharField(verbose_name="角色名",max_length=64)
    status = models.SmallIntegerField(verbose_name="状态",choices=STATUS_CHOICES,default=1)
    # auto_now:每当对象被保存时将字段设为当前日期，常用于保存最后修改时间。auto_now_add：每当对象被创建时，设为当前日期，常用于保存创建日期
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="更新时间",auto_now=True)
    permissions = models.ManyToManyField(to="Permission")

    def __str__(self):
        return self.name


# 权限详情表
class Permission(models.Model):
    title = models.CharField(verbose_name="权限名",max_length=64)
    url = models.CharField(max_length=256)

    actions = models.CharField(max_length=32)

    def __str__(self):
        return self.title

# 用户操作记录表
class App_access_log(models.Model):
    user = models.ForeignKey(to="User",on_delete=models.CASCADE)
    url = models.ForeignKey(to='Permission',on_delete = models.CASCADE)
    query_parm = models.CharField(max_length=512)
    ip = models.CharField(max_length=64)
    create_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
