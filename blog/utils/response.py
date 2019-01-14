class BaseResponse(object):
    def __init__(self):
        self.code = 200
        self.msg = ''

    @property
    def dict(self):
        return self.__dict__
