from django.urls import path
from .views import *
app_name = 'setting_sub'
urlpatterns = [
    path('subscription', SubscriptionListView.as_view(), name="Subscription"),
    path('subscription/add/<slug:id>', subscribe, name="subscribe"),


]