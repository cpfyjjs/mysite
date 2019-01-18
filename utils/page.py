"""
自定义一个分页组件
"""


class Pagination(object):
    def __init__(self, data_num, current_page, url_prefix, params, per_page=3, max_show=5):
        """

        :param data_num:数据总数
        :param current_page:当前页
        :param url_prefix:url前缀
        :param params:get请求的请求参数
        :param per_page:每页显示多少条数据
        :param max_show:页面显示多少个页码
        """
        self.data_num = data_num
        self.per_page = per_page
        self.max_show = max_show
        self.url_prefix = url_prefix

        # 把总页码算出来
        self.page_num, more = divmod(self.data_num, self.per_page)
        if more:
            self.page_num += 1

        try:
            self.current_page = int(current_page)
        except:
            self.current_page = 1

        if self.current_page > self.page_num:
            self.current_page = self.page_num

        if self.current_page <= 0:
            self.current_page = 1


        if self.max_show > self.page_num:
            self.max_show = self.page_num

        self.half_show = self.max_show // 2

        if self.current_page - self.half_show <= 1:
            self.page_start = 1
            self.page_end = self.max_show
        elif self.current_page + self.half_show >= self.page_num:
            self.page_end = self.page_num
            self.page_start = self.page_num - self.max_show + 1

        else:
            self.page_start = self.current_page - self.half_show
            self.page_end = self.current_page + self.half_show

        import copy
        self.params = copy.deepcopy(params)

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        num = self.current_page * self.per_page
        if num > self.data_num:
            num = self.data_num
        return num

    def get_html(self):
        l = []
        # 首页
        l.append('<li><a href="{}?page=1">首页</a></li>'.format(self.url_prefix))
        # 加一个上一页
        if self.current_page == 1:
            l.append('<li class="disabled"><a href="#">«</a></li>')
        else:
            self.params['page'] = self.current_page - 1
            l.append('<li><a href="{}?{}">«</a></li>'.format(self.url_prefix, self.params.urlencode()))

        # 中间页面
        for i in range(self.page_start, self.page_end + 1):
            self.params['page'] = i
            if i == self.current_page:
                l.append('<li class="disabled"><a href="#">{}</a></li>'.format(i))
            else:
                l.append('<li><a href="{0}?{1}">{2}</a></li>'.format(self.url_prefix, self.params.urlencode(), i))

        # 加一个下一页
        if self.current_page == self.page_num:
            l.append('<li class="disabled"><a href="#">»</a></li>')
        else:
            self.params['page'] = self.current_page + 1
            l.append('<li><a href="{}?{}">»</a></li>'.format(self.url_prefix, self.params.urlencode()))

        self.params['page'] = self.page_num
        l.append('<li><a href="{}?{}">尾页</a></li>'.format(self.url_prefix, self.params.urlencode()))

        return " ".join(l)
