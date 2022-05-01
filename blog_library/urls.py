from django.urls import path
from blog_library.views import *
app_name = "digital_library"
urlpatterns = [
    path('', HomeListView.as_view(), name="home"),
    # start library
    path('library', LibraryListView.as_view(), name="library"),
    path('detail/library/<slug:slug>', LibraryDetailView.as_view(), name="detail_library"),
    path('preview/library/<slug:slug>', PreviewLibrary.as_view(), name="preview_library"),
    path('library/search', LibrarySearch.as_view(), name="search_library"),
    path('category/library/<slug:slug>', category_library, name="category_library"),
    path('categorylibrary/<slug:slug>/page<int:page>', category_library, name="category_library"),
    # end library

    # start article
    path('article', ArticleListView.as_view(), name="article"),
    path('detail/article/<slug:slug>', ArticleDetailView.as_view(), name="detail_article"),
    path('preview/article/<slug:slug>', PreviewArticle.as_view(), name="preview_article"),
    path('article/search', ArticleSearch.as_view(), name="search_article"),
    path('category/article/<slug:slug>', category_article, name="category_article"),
    path('category/article/<slug:slug>/page<int:page>', category_article, name="category_article"),
    # end article
]
