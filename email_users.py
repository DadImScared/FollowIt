
import django
from django.core import mail
from pytv import Schedule

import config
import os
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'FollowIt.settings'
django.setup()
from users.models import FollowedShows


def make_time(date_str):
    return date_str.strftime('%I:%M%p')


def mail_users():
    """Gets TV schedule of today and emails each user with their followed shows that air today"""
    time = datetime.datetime.now()
    schedule = Schedule(date=time.strftime('%Y-%m-%d'))
    episode_list = [episode['show']['id'] for episode in schedule.episodes]
    shows = FollowedShows.objects.filter(show_id__in=episode_list).order_by('-air_time')
    messages = {}
    for show in shows:
        if show.user.email in messages.keys():
            messages[show.user.email].append(show)
        else:
            messages[show.user.email] = [show]
    for email, show_list in messages.items():
        mail.send_mail(
            subject="Today's shows",
            from_email=config.MAIL_USER,
            recipient_list=[email],
            message='{}'.format(
                "\n".join(['{} | {}'.format(
                    item.show_name, make_time(item.air_time)
                ) for item in show_list])
            )
        )
