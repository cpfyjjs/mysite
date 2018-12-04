import  json
from bs4 import BeautifulSoup


from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from django.contrib import auth
from django.db import transaction

from blog.models import UserInfo,Article,ArticlesDetail
from blog.utils.response import BaseResponse
# Create your views here.





class EditView(View):
    """编辑文章"""


    def get(self,requset):
        user = requset.user
        categories = requset.user.blog.category_set.all()
        tags = requset.user.blog.tag_set.all()

        ret = {"categories":categories,"tags":tags}
        return render(requset,"blog/edit.html",ret)

    def post(self,request):
        """
        提交文章
        :param request:
        :return:
        """
        md = request.POST.get('md')
        html = request.POST.get('ht')
        title = request.POST.get('title')
        cate_id = request.POST.get('cate_id')
        tag_id = request.POST.get('tag_id')

        # 利用Beautifulsoup 获取文章描述前140个词
        description = BeautifulSoup(html, 'html.parser').text.replace("\n", "")[:140]
        print(description)
        # 构建文章
        try:
            with transaction.atomic():
                art_obj=Article.objects.create(title=title,
                                       user=request.user,
                                       description=description,
                                       category_id = int(cate_id))

                art_detail_obj= ArticlesDetail.objects.create(content_md=md,
                                                              content_html=html,
                                                              article=art_obj)
        except Exception as e:
            print("错误")



        print(md,html,title,cate_id,tag_id)
        return HttpResponse("kasih")




class ArticlesView(View):
    """文章列表页"""

    def get(self,request):
        return render(request,"blog/articles.html")


    def post(self,request):
        pass