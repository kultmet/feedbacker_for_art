from django.contrib import admin

from .models import User
# Register your models here.


class AdminUser(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'role',
        'confirmation_code',
        'password',
    )

# class AdminCode(admin.ModelAdmin):
#     list_display = (
#         'pk',
#         'email',
#         'user',
#         'confirmation_code',
#     )
    
admin.site.register(User, AdminUser)
