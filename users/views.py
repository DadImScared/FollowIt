
import datetime

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from .models import FollowedShows
from .forms import SignUpForm
from .tokens import account_activation_token

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


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your FollowIt Account'
            message = render_to_string('users/account_activation_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)
            return redirect('users:account_activation_sent')
    else:
        form = SignUpForm()
    return render(request, 'users/register.html', {'form': form})


def account_activation_sent(request):
    return render(request, 'users/account_activation_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('schedule:schedules')
    else:
        return render(request, 'users/account_activation_invalid.html')
