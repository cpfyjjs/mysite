import  json
from bs4 import BeautifulSoup


from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse


from blog.models import Blog
from blog.utils.response import BaseResponse
from blog.utils import forms

class BlogView(View):
    def get(self,request):
        blog_form = forms.BlogForm()
        return render(request,'blog/add_blog.html',locals())

    def post(self,request):
        blog_form = forms.BlogForm(request.POST)
        if blog_form.is_valid():
            blog = Blog.objects.create(**blog_form.cleaned_data)
            blog.userinfo = request.user
            return


