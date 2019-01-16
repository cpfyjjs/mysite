from django.urls import path
from django.urls import include
from django.shortcuts import HttpResponse, render, redirect


class ShowList(object):
    def __init__(self, config, data_list, request):
        pass

    def get_filter_tags(self):
        pass

    def get_action_list(self):
        pass

    def get_header(self):
        pass

    def get_body(self):
        pass


class XAdminStark(object):
    list_display = ['__str__']
    list_display_links = []

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def edit(self, obj=None, header=False):
        pass

    def delete(self, obj=None, header=False):
        pass

    def checkbox(self, obj=None, header=False):
        pass

    def get_modelform_class(self):
        pass

    def new_list_play(self):
        temp = []
        temp.append(XAdminStark.checkbox)
        temp.extend(self.list_display)
        if not self.list_display_links:
            temp.append(XAdminStark.edit)
        temp.append(XAdminStark.delete)
        return temp

    def get_delete_url(self, obj):
        pass

    def get_add_url(self, obj):
        pass

    def get_list_url(self, obj):
        pass

    def get_search_condition(self, request):
        pass

    def get_filter_condition(self, request):
        pass

    def add_view(self, request):
        pass

    def delete_view(self, request, id):
        pass

    def change_view(self, request, id):
        pass

    def list_view(self, request):
        pass

        # 生成数据列表

        return render(request, 'xadmin/list_view.html', locals())

    def get_urls(self):
        temp = []
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label

        # 增加注册的model的url
        temp.append(path('add/', self.add_view, name='{0}_{1}_add'.format(app_name, model_name)))
        temp.append(path('<int:id>/delete/', self.delete_view, name='{0}_{1}_delete'.format(app_name, model_name)))
        temp.append(path('<int:id>/change/', self.change_view, name='{0}_{1}_change'.format(app_name, model_name)))
        temp.append(path('', self.list_view, name='{0}_{1}_list_view'.format(app_name, model_name)))

        # 增加用户登陆相关的url

        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None


class XAdminSite(object):
    def __init__(self):
        self._register = {}

    def register(self, model, stark_class=None):
        if not stark_class:
            stark_class = XAdminStark

        self._register[model] = stark_class(model, self)

    def get_urls(self):
        temp = []

        # 整个站点相关的url
        site_url = [
            path('', self.home_view, name='home'),
            path('login/', self.login, name='login'),
            path('logout/', self.logout, name='logout'),
            path('password_change/', self.password_change, name='password_change'),
            path('password_change/done/', self.password_change_done, name='password_change_done'),
        ]
        temp.extend(site_url)

        # 与注册模型相关的url
        for model, stark_class_obj in self._register.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            temp.append(path('{}/{}'.format(app_label, model_name), stark_class_obj.urls))

        return temp

    @property
    def urls(self):
        return include(self.get_urls())

    def home_view(self, request):
        pass

    def login(self, request):
        pass

    def logout(self, request):
        pass

    def password_change(self, request):
        pass

    def password_change_done(self, request):
        pass


site = XAdminSite()
