from django import forms
from django.core.exceptions import ValidationError
from blog import models



"""
如果模型字段设置blank=True，那么表单字段的required设置为False。 否则，required=True。
表单字段的label属性根据模型字段的verbose_name属性设置，并将第一个字母大写。
如果模型的某个字段设置了editable=False属性，那么它表单类中将不会出现该字段。
表单字段的help_text设置为模型字段的help_text。
如果模型字段设置了choices参数，那么表单字段的widget属性将设置成Select框，其选项来自模型字段的choices。选单中通常会包含一个空选项，
并且作为默认选择。如果该字段是必选的，它会强制用户选择一个选项。 如果模型字段具有default参数，则不会添加空选项到选单中。"""

class UserInfoModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"


class CategoryModelForm(forms.ModelForm):

    class Meta:
        model = models.Category
        fields = ['title','blog']
        widgets = {
            'title':forms.TextInput(attrs={'class':""})
        }
        labels = {
            'title':"文章类别",
            'blog':"所属博客",
        }
        help_texts = {
            'title':"请输入文章类别名称",
            'blog':"请输入所属博客",
        }
        error_messages = {
            'title':{
                "max_length":"文章类别名称太长"
            }
        }



class RegisterModelForm(forms.ModelForm):
    re_password = forms.CharField()

    class Meta:
        models = models.UserInfo
        fields = ['username','nickname','password','re_password','email','phone']
        # 定义显示的标签
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'nickname':forms.TextInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
            're_password':forms.PasswordInput(attrs={'class':'form-control'}),
            'email':forms.EmailInput(attrs={'class':'form-control'}),
            'phone':forms.TextInput(attrs= {'class':'form-control'}),
        }
        labels = {
            'username':"用户名",
            'nickname':"昵称",
            'password':"密码",
            're_password':"确认密码",
            'email':"邮箱",
            'phone':"电话号码",
        }

    # 重写一些字段验证的方法。
    """
    forms.ModelForm 继承自BaseForm,所以BaseForm所有的一些方法，属性。ModelForm都有如self.clean_data
    """
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
        re_password = self.cleaned_data.get("repassword")

        if re_password and re_password != password:
            self.add_error("re_password",ValidationError("两次输入的密码不一致"))
        else:
            return self.cleaned_data



