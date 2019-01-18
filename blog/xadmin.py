from xadmin.service.xadmin import site
from xadmin.service.xadmin import XAdminModel
from blog.models import Category
from blog.models import Article
from blog.models import UserInfo
from blog.models import Tag



class CategoryModel(XAdminModel):
    list_display = ['id', 'title', 'blog']


class ArticleModel(XAdminModel):
    list_display = ['id', 'title', 'user', 'create_time', 'category', 'tags']
    list_filter = ['category', 'tags']
    search_fields = ['title']


site.register(Category, CategoryModel)
site.register(Article, ArticleModel)
site.register(UserInfo)
site.register(Tag)
