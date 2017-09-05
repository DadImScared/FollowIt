from django.conf.urls import url

from . import views

app_name = 'schedule'
urlpatterns = [
    url(r'^$', views.SchedulesView.as_view(), name='schedules'),
    url(r'^(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', views.SchedulesView.as_view(), name='schedules_by_date')
]
