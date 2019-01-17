"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include, register_converter
from django.shortcuts import HttpResponse
from django.contrib import admin
from blog.views import registe
from rbac import views
from xadmin.service.xadmin import site


def login(requset):
    return HttpResponse('login')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', registe.index_view),
    path('login/', views.LoginView.as_view()),
    path('blog/', include('blog.urls')),
    path('xadmin/', site.urls),
]


def bad_request(request):
    pass


def permission_denied(request):
    pass


def pag_not_found(request):
    return HttpResponse("meiyou")


"""
自定义用户请求错误页面。
需要提前将setting.py配置文件中的Debug改为False,默认为True
"""

handler400 = bad_request
handler403 = permission_denied
handler404 = pag_not_found
# handler500 = pag_not_found
