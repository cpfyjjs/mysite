from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=32)
    pwd = models.CharField(max_length=32)

    def __str__(self):
        return self.name



class Author(models.Model):
    nickname = models.CharField(max_length=32)
    avatar = models.CharField(max_length=128)

    user = models.OneToOneField(to="User",on_delete=models.CASCADE)

    def __str__(self):
        return self.nickname




class Blog(models.Model):
    title = models.CharField(max_length=32)


    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length = 32 )
    user = models.ForeignKey(to="User",on_delete=models.CASCADE)


    def __str__(self):
        return self.title





class ArticlesDetail(models.Model):
    content = models.TextField()