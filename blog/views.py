import  json
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from django.contrib import auth
from blog.models import UserInfo
from blog.utils.response import BaseResponse
# Create your views here.

def index(request,*args,**kwargs):

    return render(request, "blog/index.html")

class LoginView(View):
    """用户登录"""

    def get(self,request):

        return render(request,"blog/login.html")

    def post(self,request):
        print("dsfaa")
        name = request.POST.get("username")
        password = request.POST.get("password")
        check = request.POST.get("check")

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

        return render(request,"blog/register.html")



class EditView(View):
    """编辑文章"""


    def get(self,requset):

        return render(requset,"blog/edit.html")

    def post(self,request):
        md = request.POST.get('md')
        print(md)
        return HttpResponse("kasih")




class ArticlesView(View):
    """文章列表页"""

    def get(self,request):
        return render(request,"blog/articles.html")


    def post(self,request):
        pass
