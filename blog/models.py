from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息表
    """

    phone =models.CharField(max_length=11,null =True,unique=True)

    def __str__(self):
        return self.username


class Author(models.Model):
    nickname = models.CharField(max_length=32)
    avatar = models.CharField(max_length=128)

    user = models.OneToOneField(to="UserInfo",on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname




class Blog(models.Model):
    title = models.CharField(max_length=32)


    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length = 32 )
    user = models.ForeignKey(to="UserInfo",on_delete=models.CASCADE)


    def __str__(self):
        return self.title





class ArticlesDetail(models.Model):
    content = models.TextField()





