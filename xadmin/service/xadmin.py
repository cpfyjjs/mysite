from collections import defaultdict
from collections import namedtuple
import copy

from django.urls import path
from django.urls import include
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import reverse
from django.db.models import Q
from django.db.models.fields.related import ManyToManyField
from django.db.models.fields.related import ForeignKey
from django.forms.boundfield import BoundField
from django.forms.models import ModelChoiceField
from django.utils.safestring import mark_safe

from utils import page
from xadmin.views.calendar import CalendarView


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
        self.app_label = self.config.model._meta.app_label
        self.model_name = self.config.model._meta.model_name

        # 分页
        data_count = self.data_list.count()
        current_page = int(self.request.GET.get('page', 1))
        base_url = self.request.path

        self.pagination = page.Pagination(data_count, current_page, base_url, self.request.GET, per_page=4, max_show=5)
        self.page_data = self.data_list[self.pagination.start:self.pagination.end]

        # actions
        self.actions = self.config.new_actions()

    # 获取过滤标签
    def get_filter_tags(self):
        """

        :return:
        """
        link_dict = {}

        for filter_field in self.config.list_filter:
            params = copy.deepcopy(self.request.GET)

            cid = self.request.GET.get(filter_field, 0)
            filter_field_obj = self.config.model._meta.get_field(filter_field)

            if isinstance(filter_field_obj, ForeignKey) or isinstance(filter_field_obj, ManyToManyField):
                print(filter_field_obj.related_model)
                """
                {'name': 'category', 'verbose_name': '所属类别', '_verbose_name': '所属类别', 
                'primary_key': False, 'max_length': None, '_unique': False, 'blank': False, 
                'null': False, 'remote_field': <ManyToOneRel: blog.article>, 'is_relation': True, 
                'default': <class 'django.db.models.fields.NOT_PROVIDED'>, 'editable': True, 
                'serialize': True, 'unique_for_date': None, 'unique_for_month': None, 
                'unique_for_year': None, 'choices': [], 'help_text': '', 'db_index': True, 
                'db_column': None, '_db_tablespace': None, 'auto_created': False, 'creation_counter': 65, 
                '_validators': [], '_error_messages': None, 
                'error_messages': {'invalid_choice': 'Value %(value)r is not a valid choice.', 'null': 'This field cannot be null.', 'blank': 'This field cannot be blank.', 'unique': '%(model_name)s with this %(field_label)s already exists.', 'unique_for_date': '%(field_label)s must be unique for %(date_field_label)s %(lookup_type)s.', 'invalid': '%(model)s instance with %(field)s %(value)r does not exist.'}, 
                'from_fields': ['self'], 
                'to_fields': [None], 'swappable': True, 'db_constraint': True, 
                'attname': 'category_id', 'column': 'category_id', 'concrete': True, 
                'model': <class 'blog.models.Article'>, 'opts': <Options for Article>, 
                
                'related_model': <class 'blog.models.Category'>, 'validators': [], 
                
                '_related_fields': [(<django.db.models.fields.related.ForeignKey: category>, <django.db.models.fields.AutoField: id>)]}"""
                data_list = filter_field_obj.related_model.objects.all()
                print(data_list)
            else:
                data_list = self.config.model.objects.all().values("pk", filter_field)

            temp = []
            # 处理全部标签
            if params.get(filter_field):
                del params[filter_field]
                temp.append("<a href='?{}'>全部</a>".format(params.urlencode()))
            else:
                temp.append("<a class='activate' href='#'>全部</a>")

            # 处理数据标签
            for obj in data_list:
                if isinstance(filter_field_obj, ManyToManyField) or isinstance(filter_field_obj, ForeignKey):
                    pk = obj.pk
                    text = str(obj)
                    params[filter_field] = pk
                else:
                    pk = obj.get("pk")
                    text = obj.get(filter_field)
                    params[filter_field] = text

                _url = params.urlencode()
                if cid == str(pk) or cid == text:
                    link_tag = "<a class='active' href='?{}'>{}</a>".format(_url, text)
                else:
                    link_tag = "<a href='?{}'>{}</a>".format(_url, text)

                temp.append(link_tag)
            link_dict[filter_field] = temp
        return link_dict

    # 获取actions
    def get_action_list(self):
        temp = []
        for action in self.actions:
            temp.append({
                "name": action.__name__,
                "desc": action.short_description,
            })

        return temp

    # 构建表头
    def get_header(self):

        header_list = []
        # header [checkbox , 'pk','name', edit, delete]
        for field in self.config.new_list_play():
            if callable(field):
                val = field(self.config, header=True)
                header_list.append(val)
            elif field == '__str__':
                header_list.append(self.config.model._meta.model_name.upper())
            else:
                val = self.config.model._meta.get_field(field).verbose_name
                header_list.append(val)
        return header_list

    # 构建表内数据
    def get_body(self):
        """

        :return:
        """
        new_data_list = []
        # 便利需要显示的表单数据
        for obj in self.page_data:
            temp = []

            for field in self.config.new_list_play():
                if callable(field):
                    # xadminmodel 内部定义的一些方法[edit ,delete]
                    val = field(self.config, obj)
                else:
                    try:
                        field_obj = self.config.model._meta.get_field(field)
                        if isinstance(field_obj, ManyToManyField):
                            # 获取所有的所对多的字段
                            ret = getattr(obj, field).all()
                            t = []
                            for m_obj in ret:
                                t.append(str(m_obj))
                            val = ",".join(t)

                        else:
                            val = getattr(obj, field)
                            if field in self.config.list_display_link:
                                #
                                _url = self.config.get_change_url(obj)
                                val = mark_safe("<a href='{}'>{}</a>".format(_url, val))
                    except Exception as e:
                        val = getattr(obj, field)
                temp.append(val)
            new_data_list.append(temp)
        return new_data_list


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
        self.model_name = self.model._meta.model_name
        self.app_label = self.model._meta.app_label

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
        if header:
            return "操作"
        _url = self.get_change_url(obj)

        return mark_safe("<a href='{}'>编辑</a>".format(_url))

    def delete(self, obj=None, header=False):
        """
        删除子类的实例
        :param obj:
        :param header:
        :return:
        """
        if header:
            return "操作"
        _url = self.get_delete_url(obj)

        return mark_safe("<a href='{}'>删除</a>".format(_url))

    def checkbox(self, obj=None, header=False):
        """
        复选框
        :param obj:
        :param header:
        :return:
        """
        if header:
            return mark_safe("<input id='choice' type='checkbox'>")
        return mark_safe("<input class='choice_item' type='checkbox' name='selected_pk' value='{}'".format(obj.pk))

    def get_modelform_class(self):
        if not self.modelform_class:
            from django.forms import ModelForm

            class ModelFormDemo(ModelForm):
                class Meta:
                    model = self.model
                    fields = "__all__"

            return ModelFormDemo
        else:
            return self.modelform_class

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
        _url = reverse("{}_{}_delete".format(self.app_label, self.model_name), args=(obj.pk,))
        return _url

    def get_change_url(self, obj):
        """
        获取编辑的url
        :param obj:
        :return:
        """
        _url = reverse("{}_{}_change".format(self.app_label, self.model_name), args=(obj.pk,))
        return _url

    def get_add_url(self):
        """
        获取添加的url
        :return:
        """
        _url = reverse("{}_{}_add".format(self.app_label, self.model_name))
        return _url

    def get_list_url(self):
        """
        获取展示的url
        :return:
        """
        _url = reverse("{}_{}_list".format(self.app_label, self.model_name))
        return _url

    def get_search_condition(self, request):
        """
        构建搜索的过滤条件
        :param request:
        :return:
        """
        key_world = request.GET.get('q')
        self.key_world = key_world

        search_connection = Q()
        if self.key_world:
            # example self.key_world = ['title', 'price']
            search_connection.connector = "or"
            for search_field in self.search_fields:
                search_connection.children.append((search_field + "__contains"), key_world)
        return search_connection

    def get_filter_condition(self, request):
        """
        构建标签的过滤条件
        :param request:
        :return:
        """
        filter_condition = Q()
        for filter_field, val in request.GET.items():
            if filter_field in self.list_filter:
                filter_condition.children.append((filter_field, val))
        return filter_condition

    def add_view(self, request):
        """
        增加数据页面的主函数
        :param request:
        :return:
        """
        ModelFormDemo = self.get_modelform_class()
        form = ModelFormDemo()

        for bfield in form:
            # print(type(bfield.field))
            if isinstance(bfield.field, ModelChoiceField):
                bfield.is_pop = True

                # bfield.field.queryset.model  一对多或者多对多字段的关联模型表
                related_model_name = bfield.field.queryset.model._meta.model_name
                related_app_label = bfield.field.queryset.model._meta.app_label

                _url = reverse('{}_{}_add'.format(related_app_label, related_model_name))
                bfield.url = _url + "?pop_res_id=id_{}".format(bfield.name)

        if request.method == "POST":
            form = ModelFormDemo(request.POST)
            if form.is_valid():
                obj = form.save()

                pop_res_id = request.GET.get("pop_res_id")
                if pop_res_id:
                    res = {"pk": obj.pk, "text": str(obj), "pop_res_id": pop_res_id}
                    import json
                    return render(request, 'xadmin/pop.html', {"res": res})

                else:
                    return redirect(self.get_list_url())

        return render(request, 'xadmin/add_view.html', {'form': form})

    def delete_view(self, request, id):
        """
        删除数据页面的主函数
        :param request:
        :param id:
        :return:
        """
        self.model.objects.filter(pk=id).delete()
        return HttpResponse('delete view')

    def change_view(self, request, id):
        """
        更改数据页面的主函数
        :param request:
        :param id:
        :return:
        """
        return HttpResponse('change_view')

    def list_view(self, request):
        """
        展示数据页面的主函数
        :param request:
        :return:
        """

        # 获取search的Q对象
        search_connection = self.get_search_condition(request)

        # 获取filter的Q对象
        filter_condition = self.get_filter_condition(request)

        # 删选获取当前表的所有数据
        data_list = self.model.objects.all().filter(search_connection).filter(filter_condition)

        # 按showlist 展示页面
        showlist = ShowList(self, data_list, request)

        return render(request, 'xadmin/list_view.html', {'showlist': showlist})

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
        return include(self.get_urls())


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

        # 与注册模型相关的url
        for model, xadmin_class_obj in self._register.items():
            model_name = model._meta.model_name
            app_label = model._meta.app_label
            temp.append(path('{}/{}/'.format(app_label, model_name), xadmin_class_obj.urls))

        # 整个站点相关的url
        from xadmin.views import account
        site_url = [
            path('', self.home_view, name='home'),
            path('login/', account.login, name='login'),
            path('logout/', account.logout, name='logout'),
            path('password_change/', account.password_change, name='password_change'),
            path('password_change/done/', account.password_change_done, name='password_change_done'),
            path('calendar/', CalendarView.as_view(), name='calendar'),
        ]
        temp.extend(site_url)

        return temp

    @property
    def urls(self):
        return include(self.get_urls())

    def home_view(self, request):
        """
        XAdminMole展示的主页面
        :param request:
        :return:
        """
        app_dict = dict()
        """
        app_dict = {
            app_name01:[model_name01,model_name02,model_name03],
            app_name02: [model_name01, model_name02, model_name03]
        }
        """
        model_url = namedtuple('model_url', 'model_name list_view add_view')

        for model, xadmin_class_obj in self._register.items():

            model_name = model._meta.model_name
            app_label = model._meta.app_label

            list_view = "/xadmin/{}/{}".format(app_label, model_name)
            add_view = "/xadmin/{}/{}/add".format(app_label, model_name)
            temp = model_url(model_name, list_view, add_view)
            if app_dict.get(app_label):
                app_dict[app_label].append(temp)
            else:
                app_dict[app_label] = [temp]
        return render(request, 'xadmin/home.html', {'app_dict': app_dict})


# 单例模式
site = XAdminSite()
