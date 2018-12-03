class BaseResponse(object):
    def __init__(self):
        self.code = 200
        self.msg = None

    @property
    def dict(self):
        self.code
        return {'code':self.code,'msg':self.msg}
