"""
博客站点所用到form类
"""

from django import forms
from django.core.exceptions import ValidationError
from blog import models



# 定义一个用户注册类
class Regsiter(forms.Form):
    username = forms.CharField(min_length=3,
                               max_length=16,
                               label= "用户名",
                               error_messages={
                                   "min_length":"用户名最小长度为3",
                                   "max_length":"用户名最大长度为16",
                                   "required":"用户名不能为空",
                               },
                               widget=forms.widgets.TextInput(
                                   attrs={"class":"form-control"},
                               ))

    nickname = forms.CharField(min_length=3,
                               max_length=32,
                               label="用户昵称",
                               error_messages={
                                   "min_length":"用户名最小长度为3",
                                   "max_length":"用户名最大长度为32",}
                               )

    password =forms.CharField(min_length=6,
                              label="密码",
                              error_messages={
                                  "min_length":"密码最小长度为6",
                                  "require":"密码不能为空"
                              },
                              widget=forms.widgets.PasswordInput(
                                  attrs={"class":"form-control"},
                              ))
    repassword = forms.CharField(min_length=6,
                               label="密码",
                               error_messages={
                                   "min_length": "密码最小长度为6",
                                   "require": "密码不能为空"
                               },
                               widget=forms.widgets.PasswordInput(
                                   attrs={"class": "form-control"},
                               ))

    email = forms.EmailField(label="邮箱",
                             error_messages={
                                 "require":"邮箱不能为空"
                             },
                             widget=forms.widgets.EmailInput(
                                 attrs={"class":"form-control"}
                             ))

    phone = forms.CharField(label="电话号码",
                            widget=forms.widgets.TextInput(
                                attrs={"class":"form-control"}
                            ))


    # 重写username字段的局部钩子函数
    def clean_username(self):
        username = self.cleaned_data.get("username")
        is_exit = models.UserInfo.objects.filter(username=username).first()

        if is_exit:
            # 用户名以存在
            self.add_error("username",ValidationError("用户名已存在"))
        else:
            return username


    # 重写email字段的局部钩子函数
    def clean_email(self):
        email = self.cleaned_data.get("email")
        is_exit = models.UserInfo.objects.filter(email=  email).first()

        if is_exit:
            # 邮箱已经被注册
            self.add_error("email",ValidationError("邮箱已经被注册"))
        return email


    # 重写phone字段的局部钩子函数
    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        #验证电话号码是否符合格式
        return phone


    # 重写全局的钩子函数
    def clean(self):

        # 校验两次输入的密码是否一致
        password = self.cleaned_data.get("password")
        repassword = self.cleaned_data.get("repassword")

        if repassword and repassword != password:
            self.add_error("repassword",ValidationError("两次输入的密码不一致"))
        else:
            return self.cleaned_data









