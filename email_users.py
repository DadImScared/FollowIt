
import django
from django.db import IntegrityError
from django.core import mail
from pytv import Schedule

import config
import os
import datetime

os.environ['DJANGO_SETTINGS_MODULE'] = 'FollowIt.settings'
django.setup()
from users.models import FollowedShows, UnwatchedEpisode


def make_time(date_str):
    return date_str.strftime('%I:%M%p')


def save_episodes(episode_list):
    """Create UnwatchedEpisode objects and save them per episode in episode_list

    :param list episode_list:
    :return:
    """
    unwatched_episodes = []
    for episode in episode_list:
        followed_shows = FollowedShows.objects.filter(show_id=episode.show.id)
        for show in followed_shows:
            unwatched_episodes.append(
                UnwatchedEpisode(
                    followed_show=show,
                    episode_id=episode.id,
                    episode_name=episode.name,
                    season=episode.season,
                    episode_number=episode.number or 0,
                    air_date=episode.airdate,
                    air_time=episode.airtime,
                    air_stamp=episode.airstamp,
                    summary=episode.summary or "no summary"
                )
            )
    try:
        UnwatchedEpisode.objects.bulk_create([
            item for item in unwatched_episodes
        ])
    except IntegrityError:
        for item in unwatched_episodes:
            try:
                item.save()
            except IntegrityError:
                continue


def mail_users():
    """Gets TV schedule of today and emails each user with their followed shows that air today"""
    time = datetime.datetime.now()
    schedule = Schedule(date=time.strftime('%Y-%m-%d'))
    episode_list = [episode.show.id for episode in schedule.episodes]
    shows = FollowedShows.objects.filter(show_id__in=episode_list,
                                         user__profile__email_confirmed=True
                                         ).order_by('-air_time')
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
    save_episodes(schedule.episodes)

if __name__ == '__main__':
    mail_users()
