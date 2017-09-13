
from django.conf.urls import url
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

from . import views


app_name = 'users'
urlpatterns = [
    url(r'^register/$', CreateView.as_view(
        template_name='users/register.html',
        form_class=UserCreationForm,
        success_url='/schedule',
    )),
    url(r'^followed/$', views.followed_shows, name='followed'),
    url(r'^followed/(?P<air_day>[a-zA-Z]+)', views.followed_shows, name='followed_day'),

]
