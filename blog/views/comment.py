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
        article_id = request.GET.get("article_id")
        comments = Comment.objects.filter(article_id=article_id)
        comments_dict = comments.values('id','user__nickname','user__avatar','article_id','content','create_time','parent_comment_id','user_id','depth')
        for item in comments_dict:
            item['create_time'] = item['create_time'].strftime("%Y-%m-%d")
        comments_dict = json.dumps(list(comments_dict))
        return HttpResponse(comments_dict)

    def post(self,request):
        ret = BaseResponse()
        user_id = request.POST.get("user_id")
        article_id = request.POST.get("article_id")
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")
        depth = 0
        try:
            if parent_id:
                depth = Comment.objects.get(id=parent_id).depth + 1
                comment_obj = Comment.objects.create(user_id=user_id,article_id=article_id,content=content,parent_comment_id=parent_id,depth=depth)
                print(depth)
            else:
                comment_obj = Comment.objects.create(user_id=user_id, article_id=article_id, content=content)
        except Exception as e:
            ret.code =100
            ret.msg = "创建评论失败"

        else:
            ret.create_time = comment_obj.create_time.strftime("%Y-%m-%d")
            ret.id = comment_obj.id

        return JsonResponse(ret.dict)

    def delete(self,request):
        ret = BaseResponse()
        delete_id = QueryDict(request.body).get('delete_id')
        try:
            Comment.objects.get(id = delete_id).delete()
        except:
            ret.code =100
            ret.msg = "删除失败"
        print(ret.dict)
        return JsonResponse(ret.dict)
