from django.contrib import admin
from datetime import timedelta,datetime
# 为整个admin站点设置默认空白显示值
admin.AdminSite.empty_value_display = "XXXXXX"

# Register your models here.

from blog import models

class UserInfoAdmin(admin.ModelAdmin):
    actions = []
    # 是否在列表上方显示actions的下拉框，默认为True
    actions_on_top = True
    # actions_on_bottom = False
    # 是否在actions下拉框右侧显示选中的对象的数量,默认为True
    actions_selection_counter = True
    # 根据你指定的日期相关的字段，为页面创建一个时间导航栏，可通过日期过滤对象
    date_hierarchy = 'last_login'


    # 指定用于链接修改页面的字段
    list_display_links = ['username']
    # 指定在修改列表页面中哪些字段可以被编辑,修改后可以直接批量保存
    list_editable = ['nickname','email','phone']
    # 设置list_filter属性后，可以激活修改列表页面的右侧边栏，用于对列表元素进行过滤
    list_filter = ['is_superuser']

    """将一个函数作为list_display的一员"""
    def last_login_interval(self,obj):
        """
        用户有多久没有在进行登陆过了
        :param obj: UserInfo 实例化对象
        :return:
        """
        data =[(1,"一天之内"),(7,"一星期之内"),(30,"一个月之内"),
               (180,"半年之内"),(365,"一年之内")]
        now = datetime.now()
        for day,value in data:
            # TODO bug  can't compare offset-naive and offset-aware datetimes
            if obj.last_login  > (now - timedelta(days=day)):
                return value
        return "一年之外"

    last_login_interval.short_description = "最近登陆"

    # 指定显示在修改页面上的字段
    list_display = ['username', 'nickname', 'email', 'phone','last_login']





class AuthorAdmin(admin.ModelAdmin):
    pass


class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','motto','theme',]



class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title','user','up_count','category','create_time']
    list_display_links = ['title']
    list_filter = ['category']


class ArticleDetailAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    list_display = ['title','blog']
    list_editable = ['blog']


class Article2TagAdmin(admin.ModelAdmin):
    pass


class ArticleUpAdmin(admin.ModelAdmin):
    pass


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user','article',]




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

