from django.urls import path
from blog import views

urlpatterns = [
    path('index/', views.index),
    path('login/', views.LoginView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('edit/', views.EditView.as_view()),

    path('articles/', views.ArticlesView.as_view()),

]