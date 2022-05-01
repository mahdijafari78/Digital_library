from django.utils import timezone
from django.utils.html import format_html
from account.models import *
from django.db import models
from extensions.utils import jalali_converter
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from setting_subscription.models import IPAddress
from django.core.exceptions import ValidationError


# Create your models here.


class LibraryManager(models.Manager):
    def published(self):
        return self.filter(status="p")


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status="p")


class CategoryManger(models.Manager):
    def active(self):
        return self.filter(status=True)


"""
start class category
"""


class LibraryCategory(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True, default=None,
                               verbose_name="دسته بندی", related_name="children")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.CharField(max_length=100, unique=True, verbose_name="آدرس دسته بندی")
    status = models.BooleanField(default=True, verbose_name="آیا نشان داده شود ")
    position = models.IntegerField(verbose_name="پوزیشن")

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = "دسته بندی کتاب خانه "
        verbose_name_plural = "دسته بندی ها کتاب خانه "
        ordering = ['parent__id', 'position']

    objects = CategoryManger()

    def count(self):
        return Library.objects.published().filter(category__in=[self]).count()

    def save(self, *args, **kwargs):
        self.slug = "-".join(self.slug.split())
        super().save(*args, **kwargs)


class ArticleCategory(models.Model):
    parent = models.ForeignKey('self', null=True, on_delete=models.SET_NULL, blank=True, default=None,
                               verbose_name="دسته بندی", related_name="children")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.CharField(max_length=100, unique=True, verbose_name="آدرس دسته بندی")
    status = models.BooleanField(default=True, verbose_name="آیا نشان داده شود ")
    position = models.IntegerField(verbose_name="پوزیشن")

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = "دسته بندی مقاله "
        verbose_name_plural = "دسته بندی ها مقاله "
        ordering = ['parent__id', 'position']

    objects = CategoryManger()

    def count(self):
        return Article.objects.published().filter(category__in=[self]).count()

    def save(self, *args, **kwargs):
        self.slug = "-".join(self.slug.split())
        super().save(*args, **kwargs)


"""
end class category
"""

"""
start class blog_library
"""


def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not ext.lower() in valid_extensions:
        raise ValidationError('فقط فایل پی دی اف اپلود شود')


class Library(models.Model):
    STATUS_LIBRARY = (
        ('p', 'منتشر شده '),
        ('d', 'پیش نویس'),
        ('i', 'در حال بررسی'),
        ('b', 'برگشت داده شده'),
    )
    title = models.CharField(max_length=200, verbose_name="عنوان کتاب")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="آدرس ")
    category = models.ManyToManyField(LibraryCategory, related_name="library", verbose_name="دسته بندی")
    descriptions = models.TextField(verbose_name="خلاصه متن کتاب ")
    thumbnail = models.ImageField(upload_to="image_library", verbose_name="عکس کتاب")
    publish = models.DateTimeField(default=timezone.now, verbose_name="انتشار")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    upload = models.FileField(upload_to='pdf', help_text="فقط فایل پی دی اف اپلود شود ",validators=[validate_file_extension])
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="library",
                               verbose_name="نویسنده")
    is_special = models.BooleanField(default=True, verbose_name="کتاب ویژه")
    status = models.CharField(max_length=1, choices=STATUS_LIBRARY, verbose_name="وضعیت")
    hits = models.ManyToManyField(IPAddress,blank=True, through='LibraryHits', related_name='hits', verbose_name= 'بازدیدها')
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = "کتابخانه"
        verbose_name_plural = "کتابخانه"
        ordering = ['-publish']

    def thumbnail_library(self):
        return format_html(
            "<img src='{}' style='border-radius: 5px;width: 100px ; height: 80px'>".format(self.thumbnail.url)
        )

    thumbnail_library.short_description = "تصویر کتاب "

    def category_library(self):
        return " , ".join([cate.title for cate in self.category.active()])

    category_library.short_description = " دسته بندی"

    def description_library(self):
        if len(self.descriptions) > 150:
            return self.descriptions[0:150] + '...'
        else:
            return self.descriptions

    description_library.short_description = 'خلاصه متن کتاب'

    objects = LibraryManager()

    def library_full_name(self):
        if self.author.get_full_name():
            return self.author.get_full_name()
        else:
            return self.author
    library_full_name.short_description = 'نویسنده'

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "انتشار"



"""
end class blog_library
"""

"""
start class Article
"""


class Article(models.Model):
    STATUS_ARTICLE = (
        ('p', 'منتشر شده '),
        ('d', 'پیش نویس'),
        ('i', 'در حال بررسی'),
        ('b', 'برگشت داده شده'),
    )
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله ")
    slug = models.SlugField(max_length=150, unique=True, verbose_name="آدرس مقاله ")
    category = models.ManyToManyField(ArticleCategory, verbose_name="دسته بندی ", related_name="article")
    descriptions = models.TextField(verbose_name="متن مقاله ")
    thumbnail = models.ImageField(upload_to="image", verbose_name="تصویر مقاله")
    publish = models.DateTimeField(default=timezone.now, verbose_name="انتشار مقاله ")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="article",
                               verbose_name="نویسنده")
    status = models.CharField(choices=STATUS_ARTICLE, max_length=1, verbose_name="وضعیت ")

    def __str__(self):
        return self.title

    class Meta():
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات "
        ordering = ['-publish']

    def thumbnail_tag(self):
        return format_html(
            "<img src='{}' style='border-radius: 5px;width: 100px ; height: 80px'>".format(self.thumbnail.url)
        )

    thumbnail_tag.short_description = " تصویر مقاله "

    def category_article(self):
        return " , ".join([cate.title for cate in self.category.active()])

    category_article.short_description = "دسته بندی"

    def description_article(self):
        if len(self.descriptions) > 150:
            return self.descriptions[0:150] + "..."
        else:
            return self.descriptions

    description_article.short_description = 'متن مقاله'

    objects = ArticleManager()

    def article_full_name(self):
        if self.author.get_full_name:
            return self.author.get_full_name()
        else:
            return self.author
    article_full_name.short_description = "نویسنده"

    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "انتشار"


"""
end class blog_library
"""


class TagLibrary(models.Model):
    library = models.ForeignKey('Library', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="برچسب")

    class Meta():
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها '


class TagArticle(models.Model):
    article = models.ForeignKey('Article', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True, verbose_name="برچسب")

    class Meta():
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب ها '


class LibraryHits(models.Model):
    library = models.ForeignKey(Library,on_delete=models.CASCADE)
    ip_address = models.ForeignKey(IPAddress, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
