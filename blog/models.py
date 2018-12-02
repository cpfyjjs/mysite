from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)

class Author(models.Model):
    nickname = models.CharField(max_length=32)
    avatar = models.CharField(max_length=128)

    user = models.OneToOneField(to="User",on_delete=models.CASCADE)

class Blog(models.Model):
    title = models.CharField(max_length=32)


class Article(models.Model):
    user = models.ForeignKey(to="User",on_delete=models.CASCADE)



class ArticlesDetail(models.Model):
    content = models.TextField()