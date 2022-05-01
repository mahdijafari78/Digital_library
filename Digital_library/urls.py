"""Digital_library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from account.views import Login, signup, activate

handler404 = 'setting_subscription.views.page_404'
urlpatterns = [
    path('admin/', admin.site.urls,name='admin'),
    path('', include('django.contrib.auth.urls')),
    path('', include('blog_library.urls')),
    path('', include('setting_subscription.urls')),
    path('login', Login.as_view(),name='login'),
    path('comment/', include('comment.urls')),
    path('sing-up/', signup,name='sing-up'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', activate,
         name='activate'),
    path('ratings/', include('star_ratings.urls', namespace='ratings')),
    path('panel/', include('account.urls')),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)


