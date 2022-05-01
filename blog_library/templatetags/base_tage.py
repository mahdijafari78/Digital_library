from django import template
from django.shortcuts import render
from django.db.models import Count, Q
from blog_library.models import LibraryCategory, ArticleCategory, Library
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType


register = template.Library()


@register.inclusion_tag('category_base/category.html')
def category_navbar():
    context = {'library': LibraryCategory.objects.active(), 'article': ArticleCategory.objects.active()}
    return context


@register.inclusion_tag('blog_library/category/category_library.html')
def category_library():
    context = {'library': LibraryCategory.objects.active()}
    return context


@register.inclusion_tag('blog_library/category/category_article.html')
def category_article():
    context = {'article': ArticleCategory.objects.active()}
    return context


@register.inclusion_tag('blog_library/library/tag/tag.html')
def popular_library():
    last_week = datetime.today() - timedelta(days=7)
    context = {'library': Library.objects.published().annotate(count=Count(
        'hits', filter=Q(libraryhits__created__gt=last_week))).order_by('-count', '-publish')[:5],
               "title" : "کتاب های پر بازدیده هفته"
               }
    return context


@register.inclusion_tag('blog_library/library/tag/tag.html')
def hot_library():
    content_id = ContentType.objects.get(app_label='blog_library', model='library')
    last_week = datetime.today() - timedelta(days=7)
    context = {'library': Library.objects.published().annotate(count=Count(
        'comments', filter=Q(comments__posted__gt=last_week))).order_by('-count', '-publish')[:5],
               "title": "کتاب های داغ هفته"
               }
    return context
