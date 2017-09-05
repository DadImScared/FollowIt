from django.shortcuts import render, HttpResponse, Http404
from django.views.generic import TemplateView
from pytv import Schedule
from pytv.tvmaze_utility import ApiError

# Create your views here.


# def index(request):
#     return render(request, 'schedule/base.html')


class SchedulesView(TemplateView):
    template_name = 'schedule/schedules.html'

    def get_context_data(self, date=None, **kwargs):
        if date:
            try:
                context = super().get_context_data(**kwargs)
                context['schedule'] = Schedule(date=date)
            except ApiError as e:
                # currently broken because of pytv code
                return Http404('<h4>Error: {}'.format(e))
        else:
            context = super().get_context_data(**kwargs)
            context['schedule'] = Schedule()
        return context
