import  json
from bs4 import BeautifulSoup


from django.shortcuts import render,HttpResponse,redirect
from django.views.generic import View
from django.http import JsonResponse
from django.contrib import auth
from django.db import transaction

from blog.models import UserInfo,Article,ArticleDetail
from blog.utils.response import BaseResponse
# Create your views here.
from blog.utils import page


class EditView(View):
    """编辑文章"""
    def get(self,requset):
        # 如果此人没有博客，新建博客
        if not requset.user.blog:
            return redirect(to='/blog/add_blog/')
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
        ret = BaseResponse()
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

                art_detail_obj= ArticleDetail.objects.create(content_md=md,
                                                              content_html=html,
                                                              article=art_obj)
        except Exception as e:
            ret.code =100
            ret.msg = "数据库保存文章失败"
        return JsonResponse(ret.dict)




class ArticlesView(View):
    """文章列表页"""

    def get(self,request):
        user_id = request.user.id
        if user_id:
            id_list =UserInfo.objects.get(id=user_id).articleup_set.values_list("article_id")
            id_list = [i for j in id_list for i in j]
        else:
            id_list =[]
        if request.GET.get('id'):
            id = request.GET.get('id')
            id = int(id)
            art_obj = Article.objects.filter(id=id).first()
            art_detail = art_obj.detail
            comments = art_obj.comment_set.all()
            return render(request,"blog/article.html",locals())
        else:
            # all_count = Article.objects.all().count()
            base_url = request.path
            current_page = request.GET.get("page")
            all_obj = Article.objects.all()
            tag_id = request.GET.get('tag_id')
            category_id = request.GET.get('category_id')
            if tag_id:
                all_obj =all_obj.filter(tags=tag_id)
            if category_id:
                all_obj =all_obj.filter(category_id =category_id)
            all_count = all_obj.count()



            pagination = page.Pagination(all_count,current_page,base_url,request.GET)
            art_objs = all_obj[pagination.start:pagination.end]
            # art_objs = Article.objects.all()[pagination.start:pagination.end]
            params = request.GET

            return render(request, "blog/articles.html", {'art_objs':art_objs,
                                                          'pagination':pagination,'params':params,'id_list':id_list})


    def post(self,request):
        pass

