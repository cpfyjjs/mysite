import copy
import urllib.parse
from django import template
from django.db.models import Count

from blog.models import Article
from blog.models import Category
from blog.models import Tag


register = template.Library()

def avatar_cut(value):
    value =str(value)
    return value.replace('blog',"")


register.filter('avatar_cut',avatar_cut)


# 定义一个右侧过滤器按钮
@register.inclusion_tag('right_menu.html')
def right_menu(params =None):

    tag_list = Tag.objects.all().annotate(count=Count("article")).values('title', 'count', 'id')
    category_list = Category.objects.all().annotate(count=Count("article")).values('title', 'count', 'id')

    if params == None:
        return {'tag_list': tag_list, 'category_list': category_list}
    else:
        params = dict(params)
        for key,value in params.items():
            params[key] = value[-1]


        tag_params = copy.deepcopy(params)
        for item in tag_list:

            tag_params['tag_id'] = item['id']

            item['link'] = urllib.parse.urlencode(tag_params)
        tag_params.pop('tag_id')
        tag_all = {'title':'全部','link':urllib.parse.urlencode(tag_params)}

        category_params = copy.deepcopy(params)
        for item in category_list:
            category_params['category_id'] = item['id']
            item['link'] = urllib.parse.urlencode(category_params)
        category_params.pop('category_id')
        category_all = {'title':'全部','link':urllib.parse.urlencode(category_params)}
        return {'tag_list': tag_list, 'category_list': category_list,'tag_all':tag_all,'category_all':category_all}









