import  json
from bs4 import BeautifulSoup


from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.http import JsonResponse,QueryDict

from blog.models import Blog,Comment
from blog.utils.response import BaseResponse
from blog.utils import forms

class CommentView(View):
    def get(self,request):

        return HttpResponse("get success")

    def post(self,request):
        ret = BaseResponse()
        user_id = request.POST.get("user_id")
        article_id = request.POST.get("article_id")
        content = request.POST.get("content")
        try:
            comment_obj = Comment.objects.create(user_id=user_id,article_id=article_id,content=content)
        except: 
            ret.code =100
            ret.msg = "创建评论失败"

        return HttpResponse("post success")