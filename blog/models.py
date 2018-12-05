from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class UserInfo(AbstractUser):
    """
    用户信息表
    """
    nickname = models.CharField(max_length=32,default="匿名用户",verbose_name="昵称")
    avatar = models.FileField(upload_to="blog/static/avatars/", default="blog/static/avatars/default.png", verbose_name="头像")
    phone =models.CharField(max_length=11,null =True,unique=True,verbose_name="电话号码",blank=True)
    blog = models.OneToOneField(to="Blog",null=True,on_delete=models.CASCADE)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Author(models.Model):
    """用户信息扩展表"""

    user = models.OneToOneField(to="UserInfo",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "作者"
        verbose_name_plural = verbose_name


class Blog(models.Model):
    """博客表"""
    title = models.CharField(max_length=32,verbose_name="博客名称")
    motto = models.CharField(max_length=128,blank=True,verbose_name="座右铭")
    theme = models.CharField(max_length=32,default="default",verbose_name="主题")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "博客"
        verbose_name_plural = verbose_name



class Article(models.Model):
    """文章表"""
    title = models.CharField(max_length = 32 )
    user = models.ForeignKey(to="UserInfo",on_delete=models.CASCADE)
    description = models.CharField(max_length=512,null=True,blank=True)
    create_time = models.DateTimeField(default = timezone.now)
    comment_count = models.IntegerField(default=0,verbose_name="评论数")
    up_count = models.IntegerField(default=0,verbose_name="点赞数")
    category = models.ForeignKey(to = "Category",on_delete=models.CASCADE,verbose_name="所属类别")
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
    content_md = models.TextField(blank=True)
    content_html = models.TextField(blank=True)
    article =models.ForeignKey(to="Article",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name


class Category(models.Model):
    """文章类别表"""
    title = models.CharField(max_length=32,verbose_name="类别")
    blog = models.ForeignKey(to="Blog",on_delete=models.CASCADE)

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
    article = models.ForeignKey(to="Article",on_delete=models.CASCADE)
    tag = models.ForeignKey(to="Tag",on_delete=models.CASCADE)

    def __str__(self):
        return "{}--{}".format(self.article.title,self.tag.title)

    class Meta:
        unique_together = (("article","tag"),)
        verbose_name = "文章 -- 标签"
        verbose_name_plural = verbose_name


class ArticleUp(models.Model):
    user = models.ForeignKey(to="UserInfo",on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article",on_delete=models.CASCADE)

    class Meta:
        verbose_name = "点赞"
        verbose_name_plural = verbose_name


class Comment(models.Model):
    user = models.ForeignKey(to ="UserInfo",on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article",on_delete=models.CASCADE)
    content = models.CharField(max_length=512,)
    create_time = models.DateTimeField()
    parent_comment = models.ForeignKey(to ="self",on_delete=models.CASCADE)

    def __str__(self):
        return self.content[:20]

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = verbose_name
