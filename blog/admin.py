from django.contrib import admin

# 为整个admin站点设置默认空白显示值
admin.AdminSite.empty_value_display = "XXXXXX"

# Register your models here.

from blog import models

class UserInfoAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


class BlogAdmin(admin.ModelAdmin):
    pass


class ArticleAdmin(admin.ModelAdmin):
    pass


class ArticleDetailAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


class Article2TagAdmin(admin.ModelAdmin):
    pass


class ArticleUpAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    pass




admin.site.register(models.UserInfo,UserInfoAdmin)
admin.site.register(models.Author,AuthorAdmin)
admin.site.register(models.Blog,BlogAdmin)
admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.ArticlesDetail,ArticleDetailAdmin)
admin.site.register(models.Category,CategoryAdmin)
admin.site.register(models.Tag,TagAdmin)
admin.site.register(models.Article2Tag,Article2TagAdmin)
admin.site.register(models.ArticleUp,ArticleUpAdmin)
admin.site.register(models.Comment,CommentAdmin)

