from django.contrib import admin
admin.ModelAdmin
# Register your models here.

from blog import models

admin.site.register(models.UserInfo)
admin.site.register(models.Author)
admin.site.register(models.Blog)
admin.site.register(models.Article)
admin.site.register(models.ArticlesDetail)
admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.Article2Tag)
admin.site.register(models.ArticleUp)
admin.site.register(models.Comment)

