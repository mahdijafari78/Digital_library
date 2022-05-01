from django.contrib import admin
from blog_library.models import *
from account.models import User

# Register your models here.


"""
start make
"""


def make_published(ModelAdmin, request, queryset):
    row_updated = queryset.update(status='p')
    if row_updated == 1:
        message_bit = "منتشره شده"
        ModelAdmin.message_user(request, "{} لیست {}".format(row_updated, message_bit))
    else:
        message_bit = "منتشره شده"
        ModelAdmin.message_user(request, "{} لیست {}".format(row_updated, message_bit))


make_published.short_description = "انتخاب منتشر شده ها"


def make_draft(ModelAdmin, request, queryset):
    row_updated = queryset.update(status='d')
    if row_updated == 1:
        message_bit = "پیش نویس شده"
        ModelAdmin.message_user(request, "{} لیست {}".format(row_updated, message_bit))
    else:
        message_bit = "پیش نویس شده"
        ModelAdmin.message_user(request, "{} لیست {}".format(row_updated, message_bit))


make_draft.short_description = "انتخاب پیش نویس شده ها"


def make_special(ModelAdmin, request, queryset):
    row_updated = queryset.update(status=True)
    if row_updated == 1:
        message_bit = "ویژه نشده"
        ModelAdmin.message_user(request, "{} لیست {}".format(row_updated, message_bit))
    else:
        message_bit = "ویژه نشده"
        ModelAdmin.message_user(request, "{} لیست {}".format(row_updated, message_bit))


make_special.short_description = "انتخاب ویژه شده ها"


def make_not_special(ModelAdmin, request, queryset):
    row_updated = queryset.update(status=False)
    if row_updated == 1:
        message_bit = "ویژه نشده"
        ModelAdmin.message_user(request, "{} لیست {}".format(row_updated, message_bit))
    else:
        message_bit = "ویژه نشده"
        ModelAdmin.message_user(request, "{} لیست {}".format(row_updated, message_bit))


make_not_special.short_description = "انتخاب ویژه نشده ها"


def make_show(ModelAdmin, request, queryset):
    row_updated = queryset.update(status=True)
    if row_updated == 1:
        message_bit = "نمایش داده"
        ModelAdmin.message_user(request, "{} دسته بندی {}".format(row_updated, message_bit))
    else:
        message_bit = "نمایش داده"
        ModelAdmin.message_user(request, "{} دسته بندی {}".format(row_updated, message_bit))


make_show.short_description = "نمایش داده ها"


def make_not_show(ModelAdmin, request, queryset):
    row_updated = queryset.update(status=False)
    if row_updated == 1:
        message_bit = "نمایش نداده "
        ModelAdmin.message_user(request, "  {} دسته بندی {}".format(row_updated, message_bit))
    else:
        message_bit = "نمایش نداده "
        ModelAdmin.message_user(request, "{} دسته بندی {}".format(row_updated, message_bit))


make_not_show.short_description = "نمایش نداده ها"

"""
start make
"""


"""
start class admin category
"""


@admin.register(LibraryCategory)
class CategoryLibraryAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']
    search_fields = ['title']
    actions = [make_show, make_not_show]
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 30


@admin.register(ArticleCategory)
class CategoryArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent', 'status']
    list_filter = ['status']
    search_fields = ['title']
    actions = [make_show, make_not_show]
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 30


"""
end class admin category
"""

"""
start class admin blog_library
"""


class TagLineLibrary(admin.TabularInline):
    model = TagLibrary
    extra = 0


@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_superuser=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ['title', 'slug', 'category_library', 'thumbnail_library', 'description_library', 'jpublish',
                    'library_full_name', 'is_special',
                    'status']
    list_filter = ['publish', 'is_special', 'status']
    search_fields = ['title', 'descriptions', 'author']
    inlines = [TagLineLibrary, ]
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-publish', '-status']
    actions = [make_published, make_draft, make_special, make_not_special]
    list_per_page = 30


"""
end class admin blog_library
"""

"""
start class admin article
"""


class TagLineArticle(admin.TabularInline):
    model = TagArticle
    extra = 0


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "author":
            kwargs["queryset"] = User.objects.filter(is_author=True, is_superuser=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    list_display = ['title', 'slug', 'category_article', 'thumbnail_tag', 'description_article', 'jpublish',
                    'article_full_name', 'status']
    list_filter = ['publish', 'status']
    search_fields = ['title', 'descriptions', 'author']
    inlines = [TagLineArticle]
    ordering = ['-publish', '-status']
    actions = [make_published, make_draft]
    prepopulated_fields = {'slug': ('title',)}
    list_per_page = 30


"""
end class admin article
"""
