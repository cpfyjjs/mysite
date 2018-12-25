from django.urls import path
from django.urls import re_path
from blog.views import registe
from blog.views import article


urlpatterns = [
    path('index/', registe.index_view),
    path('logout/', registe.logout_view),
    path('login/', registe.LoginView.as_view()),
    path('register/', registe.RegisterView.as_view()),
    path('edit/', article.EditView.as_view()),

    path('articles/', article.ArticlesView.as_view()),

]
from django.http import request