class BaseResponse(object):
    def __init__(self,code=200):
        """
        :param code: 200 表示成功
        :param msg: 用于请求失败时，返回的错误信息
        :param data: 用户请求成果时，储存返回的数据
        """
        self.code = code
        self.msg = ''
        self.data =''

    @property
    def dict(self):
        return self.__dict__
