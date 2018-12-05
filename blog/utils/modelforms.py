from django import forms
from blog import models

class UserInfoModelForm(forms.ModelForm):

    class Meta:
        model = models.UserInfo
