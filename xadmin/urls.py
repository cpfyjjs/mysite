from django.urls import path,include
from xadmin import views



urlpatterns = [

    path('layout/', views.layout),
]