class BaseResponse(object):
    def __init__(self):
        self.code = 200
        self.msg = None

    @property
    def dict(self):
        return {'code':self.code,'msg':self.msg}
