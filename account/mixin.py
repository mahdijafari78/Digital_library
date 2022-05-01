from django.http import Http404
from django.shortcuts import redirect, get_object_or_404
from blog_library.models import *


class LibraryMixin():
    def __init__(self):
        self.fields = ['title', 'slug', 'category', 'descriptions', 'thumbnail', 'publish',
                       'upload', 'is_special', 'status', 'author']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields.append('author')
        return super().dispatch(request, *args, **kwargs)


class ArticleMixin():
    def __init__(self):
        self.fields = ['title', 'slug', 'category', 'descriptions', 'thumbnail', 'publish', 'status']

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.fields.append('author')
        return super().dispatch(request, *args, **kwargs)


class FormMixin():

    def form_valid(self, form):
        if self.request.user.is_superuser:
            form.save()
        else:
            self.obj = form.save(commit=False)
            self.obj.author = self.request.user
            if not self.obj.status == 'i':
                self.obj.status = 'd'
        return super().form_valid(form)


class UserLibraryMixin():
    def dispatch(self, request, pk, *args, **kwargs, ):
        library = get_object_or_404(Library, pk=pk)
        if library.author == request.user and library.status in ['d', 'b'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("you can't see page")


class UserArticleMixin():
    def dispatch(self, request, pk, *args, **kwargs, ):
        article = get_object_or_404(Article, pk=pk)
        if article.author == request.user and article.status in ['b', 'd'] or request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("you can't see page")


class DeleteMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)


class AuthorAccessMixin():
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            if user.is_superuser or user.is_author:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect('panel:profile')
        else:
            return redirect("login")
