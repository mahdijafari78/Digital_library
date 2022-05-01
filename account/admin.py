from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User


# Register your models here.
def make_author(ModelAdmin, request, queryset):
    row_updated = queryset.update(is_author=True)
    if row_updated == 1:
        message_bit = "نویسنده شده"
        ModelAdmin.message_user(request, "{} کاربر {}".format(row_updated, message_bit))
    else:
        message_bit = "نویسنده شده"
        ModelAdmin.message_user(request, "{} کاربر {}".format(row_updated, message_bit))


make_author.short_description = 'انتخاب نویسنده ها '
UserAdmin.fieldsets[1][1]['fields'] = (
    'first_name',
    'last_name',
    'email',
    'image',

)
UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_superuser',
    'is_author',
    'special_user',
    'groups',
    'user_permissions',

)
UserAdmin.actions = [make_author]
UserAdmin.list_display += ('is_superuser', 'is_author','is_special_user')
UserAdmin.list_filter += ('is_author',)
admin.site.register(User, UserAdmin)
