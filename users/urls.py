
from django.conf.urls import url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views


app_name = 'users'
urlpatterns = [
    url(r'^register/$', views.signup, name='register'),
    url(r'^followed/$', views.followed_shows, name='followed'),
    url(r'^followed/(?P<air_day>[a-zA-Z]+)/$', views.followed_shows, name='followed_day'),
    url(r'^account_activation_sent/$', views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
