from django import template

register = template.Library()

def avatar_cut(value):
    value =str(value)
    return value.replace('blog',"")


register.filter('avatar_cut',avatar_cut)