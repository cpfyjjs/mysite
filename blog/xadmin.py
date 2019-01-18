from xadmin.service.xadmin import site
from xadmin.service.xadmin import XAdminModel
from blog.models import Category
from blog.models import Article
from blog.models import UserInfo
from blog.models import Tag
from blog.models import Author
from blog.models import Blog
from blog.models import ArticleDetail
from blog.models import Article2Tag
from blog.models import ArticleUp
from blog.models import Comment



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
site.register(Author)
site.register(Blog)
site.register(ArticleDetail)
site.register(ArticleUp)
site.register(Article2Tag)
site.register(Comment)
