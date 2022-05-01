from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import *
from django.contrib.auth.views import LoginView
from .mixin import *
from blog_library.models import *
from django.urls import reverse_lazy
from .models import *
from .forms import ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage


# Create your views here.

class PanelHome(AuthorAccessMixin,TemplateView):
    template_name = 'registration/panel_home.html'


"""

star panel blog_library

"""


class LibraryPanelListView(AuthorAccessMixin, ListView):
    template_name = 'registration/library/panel_library.html'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Library.objects.all()
        else:
            return Library.objects.filter(author=user)


class SearchLibraryPanel(AuthorAccessMixin, ListView):
    template_name = 'registration/library/search_panel_library.html'
    paginate_by = 20

    def get_queryset(self):
        user_library = self.request.user
        query = self.request.GET.get('q')
        if user_library.is_superuser:
            return Library.objects.filter(Q(title__icontains=query) | Q(descriptions__icontains=query))
        else:
            return Library.objects.filter(Q(title__icontains=query) | Q(descriptions__icontains=query)
                                          , author=user_library)


class LibraryCreateView(LibraryMixin, FormMixin, AuthorAccessMixin, CreateView):
    model = Library
    template_name = 'registration/library/library-create-update.html'
    success_url = reverse_lazy('panel:library')


class LibraryUpdateView(LibraryMixin, UserLibraryMixin, FormMixin, AuthorAccessMixin, UpdateView):
    model = Library
    template_name = 'registration/library/library-create-update.html'
    success_url = reverse_lazy('panel:library')


class LibraryDeleteView(DeleteMixin, DeleteView):
    model = Library
    template_name = 'registration/library/library_confirm_delete.html'
    success_url = reverse_lazy('panel:library')


"""

end panel blog_library

"""

"""

star panel article

"""


class ArticlePanelListView(AuthorAccessMixin, ListView):
    template_name = 'registration/article/panel_article.html'
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser:
            return Article.objects.all()
        else:
            return Article.objects.filter(author=user)


class SearchArticlePanel(AuthorAccessMixin, ListView):
    template_name = 'registration/article/search_panel_article.html'
    paginate_by = 20

    def get_queryset(self):
        user_article = self.request.user
        query = self.request.GET.get('q')
        if user_article.is_superuser:
            return Article.objects.filter(Q(title__icontains=query) | Q(descriptions__icontains=query))
        else:
            return Article.objects.filter(Q(title__icontains=query) | Q(descriptions__icontains=query),
                                          author=user_article)


class ArticleCreateView(ArticleMixin, FormMixin, AuthorAccessMixin, CreateView):
    template_name = "registration/article/article-create-update.html"
    model = Article
    success_url = reverse_lazy('panel:article')


class ArticleUpdateView(ArticleMixin, UserArticleMixin, FormMixin, AuthorAccessMixin, UpdateView):
    template_name = "registration/article/article-create-update.html"
    model = Article
    success_url = reverse_lazy('panel:article')


class ArticleDeleteView(DeleteMixin,DeleteView):
    model = Article
    template_name = 'registration/article/article_confirm_delete.html'
    success_url = reverse_lazy('panel:article')


"""

end panel article

"""


"""

end panel login and profile

"""


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "registration/profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy('panel:home')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_author:
            return reverse_lazy('panel:home')
        else:
            return reverse_lazy('panel:profile')


"""

end panel login and profile

"""


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'اکانت خود را فعال کنید.'
            message = render_to_string('registration/account_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/account_active.html')
    else:
        form = SignupForm()
    return render(request, 'registration/sign-up.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        # return redirect('home')
        return render(request, 'registration/account_complete.html')
    else:
        return render(request, 'registration/account_failed.html')