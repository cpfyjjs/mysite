from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.shortcuts import redirect



class AuthMiddleware(MiddlewareMixin):
    """
    定义一个用户登陆验证的模块
    """

    def process_request(self,request):
        if request.path == "/blog/edit/":
            if not request.user.username:
                return redirect(to='/blog/index')