from datetime import timedelta
import datetime

from django.shortcuts import render
from django.views.generic import ListView
from .mixin import LoginSubMixin
from account.models import User
from .models import *


# Create your views here.

def page_404(request, exception):
    return render(request, '404.html')


class SubscriptionListView(LoginSubMixin, ListView):
    queryset = Subscription.objects.filter(status=True)
    template_name = 'subscription/subscriptions.html'


def subscribe(request, id):
    today = datetime.datetime.now()
    sub = Subscription.objects.get(id=id)
    d = timedelta(days=sub.time)
    user = User.objects.get(pk=request.user.pk)
    if user.special_user == today or user.special_user > today:
        user.special_user += d
        user.save()
    else:
        user.special_user = today+d
        user.save()
    return render(request, 'subscription/add_sub.html')
