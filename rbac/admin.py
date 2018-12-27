from django.contrib import admin
from .models import User,Role,Permission,App_access_log
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['user_info']

class RoleAdmin(admin.ModelAdmin):
    list_display = ['name','status','create_time','update_time']

class PermissionAdmin(admin.ModelAdmin):
    list_display = ['title','url','actions']

class AppAdmin(admin.ModelAdmin):
    list_display = ['user','url','ip','create_time']

admin.register(User,UserAdmin)
admin.register(Role,RoleAdmin)
admin.register(Permission,PermissionAdmin)
admin.register(App_access_log,AppAdmin)