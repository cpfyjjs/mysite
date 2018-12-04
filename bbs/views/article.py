import  json
from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from django.contrib import auth
from bbs.models import UserInfo
from bbs.utils.response import BaseResponse
# Create your views here.





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