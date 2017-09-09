
import datetime

from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

from .models import FollowedShows

# Create your views here.

days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday']


def prev_day(day):
    return days[days.index(day)-1]


def next_day(day):
    return days[days.index(day)+1] if days.index(day) < len(days) - 1 else days[0]


@login_required
def followed_shows(request, air_day=None):
    """View to display shows followed by user"""
    day = air_day or datetime.datetime.now().strftime('%A')
    day = day.lower()
    shows = FollowedShows.objects.filter(user=request.user, air_days__contains=day)
    return render(
        request,
        'users/followed.html',
        {
            'shows': shows,
            'current_day': day,
            'prev_day': prev_day(day),
            'next_day': next_day(day)
         }
    )
