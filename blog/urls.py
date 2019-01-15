from django.urls import path
from django.urls import re_path
from blog.views import registe
from blog.views import article
from blog.views import blog
from blog.views import comment
from blog.views import about


app_name = "blog"

urlpatterns = [
    path('index/', registe.index_view),
    path('logout/', registe.logout_view),
    path('login/', registe.LoginView.as_view()),
    path('register/', registe.RegisterView.as_view()),
    path('edit/', article.EditView.as_view()),

    path('articles/', article.ArticlesView.as_view()),
    path('add_blog/', blog.BlogView.as_view()),
    path('category/', blog.CategoryView.as_view()),
    path('tag/', blog.TagView.as_view()),
    path('comment/', comment.CommentView.as_view()),
    path('article_up/', about.ArticleUpView.as_view()),

]
