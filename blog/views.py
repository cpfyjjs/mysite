from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from blog.models import UserInfo
from django.contrib import auth
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

        if user_object:
            print('df')
            auth.login(request,user_object)
            return redirect(to="/blog/index")

        else:
            return HttpResponse("hanhjui")


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
