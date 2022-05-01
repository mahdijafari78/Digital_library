from django.contrib import admin
from .models import *


# Register your models here.


def make_show_sub(ModelAdmin, request, queryset):
    row_updated = queryset.update(is_author=True)
    if row_updated == 1:
        message_bit = "نمایش داده شده"
        ModelAdmin.message_user(request, "{} اشتراک {}".format(row_updated, message_bit))
    else:
        message_bit = "نمایش داده شده"
        ModelAdmin.message_user(request, "{} اشتراک {}".format(row_updated, message_bit))


make_show_sub.short_description = 'انتخاب نمایش داده ها '

"""
start SubscriptionAdmin
"""


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description_sub', 'time', 'price', 'discount', 'jpublish', 'status']
    list_filter = ['status', 'publish']
    search_fields = ['name']
    list_per_page = 30
    actions = [make_show_sub]


"""
end SubscriptionAdmin
"""


"""
start IPAddressAdmin
"""


@admin.register(IPAddress)
class IPAddressAdmin(admin.ModelAdmin):
    list_display = ['ip_address']
    search_fields = ['ip_address']


"""
end IPAddressAdmin
"""