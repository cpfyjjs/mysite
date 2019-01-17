from django.urls import path
from django.urls import include
from django.shortcuts import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import reverse

from utils import page


class ShowList(object):
    def __init__(self, config, data_list, request):
        """
        为list_view.html提供数据
        :param config: 配置类,XAdminModel的子类
        :param data_list:查询结果queryset
        :param request:请求相关
        """
        self.config = config
        self.data_list = data_list
        self.request = request

        # 分页
        data_count = self.data_list.count()
        current_page = int(self.request.get('page', 1))
        base_url = self.request.path

        self.pagination = page.Pagination(data_count, current_page, base_url, self.request.GET, per_page=4, max_show=5)
        self.page_data = self.data_list[self.pagination.start:self.pagination.end]

        # actions
        self.actions = self.config.new_actions()

    # 获取过滤标签
    def get_filter_tags(self):
        pass

    # 获取actions
    def get_action_list(self):
        pass

    # 构建表头
    def get_header(self):
        pass

    # 构建表内数据
    def get_body(self):
        pass


class XAdminModel(object):
    list_display = ['__str__']
    list_display_links = []
    modelform_class = None
    search_fields = []
    actions = []
    list_filter = []

    def __init__(self, model, site):
        """
        model 的配置类
        :param model: Model的子类
        :param site: XAdminSite的子类
        """
        self.model = model
        self.site = site

    def patch_delete(self, request, queryset):
        """
        将选择的数据批量的删除
        :param request:
        :param queryset:
        :return:
        """
        queryset.delete()

    patch_delete.short_description = "批量删除"

    def edit(self, obj=None, header=False):
        """
        编辑model子类的实例
        :param obj:model子类的实例
        :param header:是否是表头
        :return:
        """
        pass

    def delete(self, obj=None, header=False):
        """
        删除子类的实例
        :param obj:
        :param header:
        :return:
        """
        pass

    def checkbox(self, obj=None, header=False):
        """
        复选框
        :param obj:
        :param header:
        :return:
        """
        pass

    def get_modelform_class(self):
        pass

    def new_list_play(self):
        """

        :return:
        """
        temp = []
        temp.append(XAdminModel.checkbox)
        temp.extend(self.list_display)
        if not self.list_display_links:
            temp.append(XAdminModel.edit)
        temp.append(XAdminModel.delete)
        return temp

    def new_actions(self):
        """

        :return:
        """
        temp = []
        temp.append(XAdminModel.patch_delete)
        temp.extend(self.actions)

        return temp

    def get_delete_url(self, obj):
        """
        获取删除的url
        :param obj:
        :return: url
        """
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("{}_{}_delete".format(app_label, model_name), kwargs={id: obj.pk})

        return _url

    def get_change_url(self, obj):
        """
        获取编辑的url
        :param obj:
        :return:
        """
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("{}_{}_change".format(app_label, model_name), kwargs={id: obj.pk})

    def get_add_url(self):
        """
        获取添加的url
        :return:
        """
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("{}_{}_add".format(app_label, model_name))

        return _url

    def get_list_url(self):
        """
        获取展示的url
        :return:
        """
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label

        _url = reverse("{}_{}_list".format(app_label, model_name))

        return _url

    def get_search_condition(self, request):
        pass

    def get_filter_condition(self, request):
        pass

    def add_view(self, request):
        """

        :param request:
        :return:
        """
        pass

    def delete_view(self, request, id):
        """

        :param request:
        :param id:
        :return:
        """
        pass

    def change_view(self, request, id):
        """

        :param request:
        :param id:
        :return:
        """
        pass

    def list_view(self, request):
        """

        :param request:
        :return:
        """


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
            stark_class = XAdminModel

        self._register[model] = stark_class(model, self)

    def get_urls(self):
        """
        二级路由分发，
        :return:
        """
        temp = []

        # 整个站点相关的url
        from xadmin.views import account
        site_url = [
            path('', self.home_view, name='home'),
            path('login/', account.login, name='login'),
            path('logout/', account.logout, name='logout'),
            path('password_change/', account.password_change, name='password_change'),
            path('password_change/done/', account.password_change_done, name='password_change_done'),
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




site = XAdminSite()
