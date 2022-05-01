from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import *
from .models import *

# Create your views here.


"""
 start home
"""


class HomeListView(ListView):
    template_name = 'blog_library/home_digital_library.html'
    paginate_by = 20
    queryset = Library.objects.published()


"""
 end home
"""

"""
start library
"""


class LibraryListView(ListView):
    queryset = Library.objects.published()
    template_name = 'blog_library/library/library.html'
    paginate_by = 10


class LibraryDetailView(DetailView):
    template_name = 'blog_library/library/detail-library.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        library = get_object_or_404(Library.objects.published(), slug=slug)
        ip_address = self.request.user.ip_address
        if ip_address not in library.hits.all():
            library.hits.add(ip_address)
        return library


class PreviewLibrary(DetailView):
    template_name = 'blog_library/library/preview_library.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Library, slug=slug)


class LibrarySearch(ListView):
    template_name = 'blog_library/library/search_library.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q_library')
        return Library.objects.filter(Q(title__icontains=query) | Q(descriptions__icontains=query))


def category_library(request,slug,page=1):
    category = get_object_or_404(LibraryCategory.objects.active(),slug=slug)
    library_list = category.library.published()
    paginator = Paginator(library_list, 10)
    library = paginator.get_page(page)
    context = {
        'category_library': category,
        'object_list': library
    }
    return render(request, 'blog_library/library/library_category.html', context)

"""
end library
"""

"""
start article
"""


class ArticleListView(ListView):
    queryset = Article.objects.published()
    template_name = 'blog_library/article/article.html'
    paginate_by = 10


class ArticleDetailView(DetailView):
    template_name = 'blog_library/article/detail-article.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article.objects.published(), slug=slug)


class PreviewArticle(DetailView):
    template_name = 'blog_library/article/preview_article.html'

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Article, slug=slug)


class ArticleSearch(ListView):
    template_name = 'blog_library/article/search_article.html'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q_article')
        return Article.objects.filter(Q(title__icontains=query) | Q(descriptions__icontains=query))


def category_article(request,slug,page=1):
    category = get_object_or_404(ArticleCategory.objects.active(),slug=slug)
    article_list = category.article.published()
    paginator = Paginator(article_list, 10)
    article = paginator.get_page(page)
    context = {
        'category_article': category,
        'object_list': article
    }
    return render(request,'blog_library/article/article_category.html', context)


"""
end article
"""

