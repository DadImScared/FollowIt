from django.shortcuts import render, HttpResponse, Http404
from django.views.generic import TemplateView
from datetime import datetime, timedelta
from pytv import Schedule
from pytv.tvmaze_utility import ApiError

# Create your views here.


# def index(request):
#     return render(request, 'schedule/base.html')


def offset_date(date, offset):
    return (date + timedelta(days=offset)).strftime('%Y-%m-%d')


class SchedulesView(TemplateView):
    template_name = 'schedule/schedules.html'

    def get_context_data(self, date=None, **kwargs):
        if date:
            try:
                current_day = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise Http404
        else:
            current_day = datetime.now()
        today = datetime.now()
        context = super().get_context_data(**kwargs)
        context['schedule'] = Schedule(date=current_day.strftime('%Y-%m-%d'))
        context['today'] = today.strftime('%Y-%m-%d')
        context['current_day'] = current_day.strftime('%a, %Y-%m-%d')
        context['prev_day'] = offset_date(current_day, -1)
        context['next_day'] = offset_date(current_day, 1)
        context['prev_week'] = offset_date(current_day, -7)
        context['next_week'] = offset_date(current_day, 7)
        return context
