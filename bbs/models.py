from django.db import models
from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    """
    用户信息表
    """
    nickname = models.CharField(max_length=32,default="匿名用户")
    avatar = models.CharField(max_length=128,default="default.jpg")
    phone =models.CharField(max_length=11,null =True,unique=True)

    def __str__(self):
        return self.username


class Author(models.Model):
    """用户信息扩展表"""

    user = models.OneToOneField(to="UserInfo",on_delete=models.CASCADE)


class Blog(models.Model):
    """博客表"""
    title = models.CharField(max_length=32)
    motto = models.CharField(max_length=128)
    theme = models.CharField(max_length=32,default="default")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name



class Article(models.Model):
    """文章表"""
    title = models.CharField(max_length = 32 )
    user = models.ForeignKey(to="UserInfo",on_delete=models.CASCADE)
    description = models.CharField(max_length=512,null=True)
    create_time = models.DateTimeField()
    comment_cont = models.IntegerField(default=0,verbose_name="评论数")
    up_cont = models.IntegerField(default=0,verbose_name="点赞数")
    category = models.ForeignKey(to = "Category",verbose_name="所属类别")
    # 中介模型
    tags = models.ManyToManyField(to = "Tag",
                                  through="Article2Tag",
                                  through_fields=("article","tag"))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name


class ArticlesDetail(models.Model):
    content = models.TextField()
    article =models.ForeignKey(to="Article")

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name


class Category(models.Model):
    """文章类别表"""
    title = models.CharField(max_length=32,verbose_name="类别")
    blog = models.ForeignKey(to="Blog")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章类别"
        verbose_name_plural = verbose_name


class Tag(models.Model):
    """文章标签表"""
    title = models.CharField(max_length=32,verbose_name="标签")
    blog = models.ForeignKey(to="Blog",on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "文章标签"
        verbose_name_plural = verbose_name


class Article2Tag(models.Model):
    pass



class ArticleUp(models.Model):
    user = models.ForeignKey(to="UserInfo",on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name




