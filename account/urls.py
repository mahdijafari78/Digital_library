from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import *
app_name = "panel"
urlpatterns = [
    path('', PanelHome.as_view(), name="home"),
    # start panel library
    path('blog_library', LibraryPanelListView.as_view(), name="library"),
    path('blog_library/search', SearchLibraryPanel.as_view(), name="search-library"),
    path('blog_library/create', LibraryCreateView.as_view(), name="library-create"),
    path('blog_library/update/<int:pk>', LibraryUpdateView.as_view(), name="library-update"),
    path('blog_library/delete/<int:pk>', LibraryDeleteView.as_view(), name="library-delete"),

    # end panel library

    # start panel Article
    path('article', ArticlePanelListView.as_view(), name="article"),
    path('article/search', SearchArticlePanel.as_view(), name="search-article"),
    path('article/create', ArticleCreateView.as_view(), name="article-create"),
    path('article/update/<int:pk>', ArticleUpdateView.as_view(), name="article-update"),
    path('article/delete/<int:pk>', ArticleDeleteView.as_view(), name="article-delete"),

    # end panel Article
    path('profile', Profile.as_view(), name="profile"),


]
