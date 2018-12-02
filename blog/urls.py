from django.conf.urls import url
from blog import views

urlpatterns = [
    url(r'^index/', views.index),
    url(r'^edit/', views.EditView.as_view()),

]