from django.shortcuts import render
from django.views.generic import View
# Create your views here.

def index(request,*args,**kwargs):

    return render(request, "blog/index.html")


class EditView(View):

    def get(self,requset,*args,**kwargs):
        return render(requset,"blog/edit.html")
