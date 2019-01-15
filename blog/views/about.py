import  json
from bs4 import BeautifulSoup


from django.db.models import F
from django.views.generic import View
from django.http import JsonResponse

from blog.utils.response import BaseResponse
from blog.models import ArticleUp
from blog.models import Article

class ArticleUpView(View):
    """点赞"""
    def post(self,requset):
        # 如果此人没有博客，新建博客
        ret = BaseResponse()
        user_id = requset.user.id
        article_id = requset.POST.get("article_id")
        print(user_id,article_id)
        article_up = ArticleUp.objects.filter(user_id=user_id,article_id=article_id)
        if article_up:
            ret.code = 100
            article_up.delete()
            Article.objects.filter(id=article_id).update(up_count=F('up_count') - 1)
            return JsonResponse(ret.dict)
        try:
            ArticleUp.objects.create(user_id=user_id, article_id=article_id)
            Article.objects.filter(id=article_id).update(up_count=F('up_count')+1)
        except:
            ret.cdoe =300
            ret.msg = "点赞失败"
        return JsonResponse(ret.dict)