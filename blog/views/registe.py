import  json
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from django.contrib import auth
from blog.models import UserInfo
from blog.utils.response import BaseResponse
from blog.utils.forms import RegsiterForm

def index_view(request,*args,**kwargs):

    return render(request, "blog/index.html")

def logout_view(request):
    """
    用户登出
    :param request:
    :return:
    """
    auth.logout(request)
    return  redirect(to='/blog/index/')





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

        ret=BaseResponse()
        if user_object:
            auth.login(request,user_object)
        else:
            ret.code = 300
            ret.msg = '用户名密码错误'

        return HttpResponse(json.dumps(ret.dict))


class RegisterView(View):
    """用户注册"""

    def get(self,request):
        form_obj = RegsiterForm()

        return render(request,"blog/register.html",locals())

    def post(self,request):
        pass

