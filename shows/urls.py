
from django.conf.urls import url

from . import views

app_name = 'shows'
urlpatterns = [
    url(r'^(?P<show_id>[0-9]+)$', views.ShowView.as_view(), name="show"),
    url(r'^follow/', views.follow_shows, name='follow_show')
]
