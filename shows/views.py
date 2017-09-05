from django.shortcuts import render, Http404
from django.http import JsonResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from pytv import Show
from pytv.tvmaze import ApiError

from users.models import FollowedShows, Person

# Create your views here.


class ShowView(TemplateView):
    """View class for shows"""

    template_name = 'shows/index.html'

    def get_context_data(self, show_id, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
            context['show'] = Show(show_id=show_id)
        except ApiError:
            raise Http404
        else:
            return context


@login_required
def follow_shows(request):
    if request.method == 'POST':
        data = request.POST
        show_id = data.get('show')
        person = Person.objects.get(pk=request.user.pk)
        if person.is_following(show_id=show_id):
            followed_show = FollowedShows.objects.get(user=person, show_id=show_id)
            followed_show.delete()
            return JsonResponse({"following": False})
        else:
            try:
                show = Show(show_id=show_id)
            except ApiError:
                raise Http404
            else:
                FollowedShows.objects.create(
                    user=person,
                    show_id=show.show_id,
                    show_name=show.name,
                    network=show.network['name'],
                    summary=show.summary,
                    air_time=show.schedule['time'],
                    air_days=",".join(show.schedule['days'])
                )
                return JsonResponse({"following": True})
