import json

from django.shortcuts import render,HttpResponse
from django.views import View
from django.contrib import auth

# Create your views here.

# 用户登陆
class LoginView(View):
    """用户登录"""

    def get(self,request):
        return render(request,"blog/login.html")

    def post(self,request):
        name = request.POST.get("username")
        password = request.POST.get("password")
        check = request.POST.get("check")
        # 利用auth模块进行用户认证
        user_object = auth.authenticate(username=name,password=password)

        ret={'code':200,'msg':""}
        if user_object:
            auth.login(request,user_object)
            # 用于初始化用户的权限列表
            init_session(request,user_object)
        else:
            ret.code = 300
            ret.msg = '用户名密码错误'

        return HttpResponse(json.dumps(ret))

def init_session(request,user):
    pass