from xadmin.service.xadmin import site

from xadmin.models import User
from xadmin.models import Role
from xadmin.models import Permission
from xadmin.models import App_access_log


# 在XAdmin注册model

site.register(User)
site.register(Role)
site.register(Permission)
site.register(App_access_log)