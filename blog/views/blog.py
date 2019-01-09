import  json
from bs4 import BeautifulSoup


from django.shortcuts import render,HttpResponse
from django.views.generic import View
from django.http import JsonResponse,QueryDict


from blog.models import Blog,Category,Tag
from blog.utils.response import BaseResponse
from blog.utils import forms

class BlogView(View):
    def get(self,request):
        blog_form = forms.BlogForm()
        return render(request,'blog/add_blog.html',locals())

    def post(self,request):
        ret = BaseResponse()
        blog_form = forms.BlogForm(request.POST)
        if blog_form.is_valid():
            blog = Blog.objects.create(**blog_form.cleaned_data)
            blog.userinfo = request.user
            blog.save()
            return JsonResponse(data=ret.dict)
        else:
            ret.code =100
            ret.msg = blog_form.errors
            return JsonResponse(data=ret.dict)


class CategoryView(View):
    def get(self,request):
        user = request.user
        categories = user.blog.category_set.all().values("id","title")
        categories = list(categories)
        cates = json.dumps(categories)
        return HttpResponse(cates)

    def post(self,request):
        ret = BaseResponse()
        title = request.POST.get('category')
        cate_obj = Category.objects.filter(title=title).first()
        if cate_obj:
            ret.code = 100
            return JsonResponse(ret.dict)
        cate_obj =Category.objects.create(title=title,blog=request.user.blog)
        return JsonResponse(ret.dict)


class TagView(View):
    def get(self,request):
        user = request.user
        tags = user.blog.tag_set.all().values("id","title")
        tags = json.dumps(list(tags))
        return HttpResponse(tags)

    def post(self, request):
        ret = BaseResponse()
        title = request.POST.get('tag')
        tag_obj = Tag.objects.filter(title=title).first()
        if tag_obj:
            ret.code = 100
            return JsonResponse(ret.dict)
        tag_obj = Tag.objects.create(title=title, blog=request.user.blog)
        id = tag_obj.id
        ret.msg = id
        return JsonResponse(ret.dict)


    def delete(self,request):
        ret = BaseResponse()
        id = QueryDict(request.body).get('id')
        try:
            tag_obj =Tag.objects.filter(id=id).delete()
        except:
            ret.code = 100
        return JsonResponse(ret.dict)