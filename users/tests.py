
import datetime
import random
from django.test import TestCase, override_settings, TransactionTestCase
from django.urls import reverse
from django.core import mail
from .models import Person, FollowedShows, Profile, UnwatchedEpisode, User
from pytv import Schedule
from email_users import mail_users, save_episodes
# Create your tests here.
# show_name=episode['show']['name'],
#             network=episode['show']['network']['name'],
#             air_time=episode['airtime'] or '00:00',
#             air_days=','.join(episode['show']['schedule']['days']).lower(),
#             summary=episode['summary'] or 'no summary'


def create_shows(user, schedule=Schedule()):
    """creates test followed shows"""
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']
    for episode in schedule.episodes:
        FollowedShows.objects.get_or_create(
            user=user,
            show_id=episode.show.id,
            defaults={
                'show_name': episode.show.name,
                'network': episode.show.network['name'],
                'air_time': episode.airtime or '00:00',
                'air_days': ','.join(episode.show.schedule['days']).lower(),
                'summary': episode.summary or 'no summary'
            }
        )


class PersonTests(TestCase):
    def test_person_is_following(self):
        """is_following should return FollowedShows object if True else None"""
        person = Person.objects.create(
            username='tom', email='tom@gmail.com', password='fake_password'
        )
        self.assertFalse(person.is_following(1))
        show = FollowedShows.objects.create(
            user=person,
            show_name='show1',
            show_id=1,
            air_days='monday, tuesday',
            air_time='10:00',
            summary='summary here',
            network='network here'
        )
        self.assertTrue(person.is_following(show.show_id))


class FollowedShowsTests(TransactionTestCase):
    def setUp(self):
        self.user = Person.objects.create_user(username='foo', password='bar', email='foo@test.com')
        self.user.save()
        Profile.objects.create(user=self.user, email_confirmed=True)
        self.user2 = Person.objects.create_user(username='bar', password='foo', email='bar@test.com')
        self.user2.save()
        Profile.objects.create(user=self.user2, email_confirmed=True)
        time = datetime.datetime.now()
        self.schedule = Schedule(date=time.strftime('%Y-%m-%d'))
        create_shows(self.user, self.schedule)
        create_shows(self.user2, self.schedule)
        self.episode_list = [episode.show.id for episode in self.schedule.episodes]
        self.shows = FollowedShows.objects.filter(show_id__in=self.episode_list).order_by('-air_time')

    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_email_users_followed_shows_on_specific_day(self):
        """Users following shows should receive an email with the shows"""
        mail_users()
        self.assertEqual(2, len(mail.outbox))
        for show in FollowedShows.objects.filter(user_id=self.user.id):
            self.assertTrue(show.unwatchedepisode_set.all().count() > 0)

    def test_save_unwatched_episodes(self):
        """Followed shows' episodes should be saved to an unwatched list"""
        save_episodes(self.schedule.episodes)
        for show in FollowedShows.objects.filter(user_id=self.user.id):
            self.assertTrue(show.unwatchedepisode_set.all().count() > 0)

    def test_save_repeat_unwatched_episodes_should_not_be(self):
        """Repeat unwatched episodes should not be saved"""
        episode = self.schedule.episodes[0]
        all_episodes = self.schedule.episodes
        followed_show = FollowedShows.objects.get(user=self.user, show_id=episode.show.id)
        UnwatchedEpisode(
            followed_show=followed_show,
            episode_id=episode.id,
            episode_name=episode.name,
            season=episode.season,
            episode_number=episode.number or 0,
            air_date=episode.airdate,
            air_time=episode.airtime,
            air_stamp=episode.airstamp,
            summary=episode.summary or "no summary"
        ).save()
        save_episodes(self.schedule.episodes)
        # make sure all episodes are saved to both users unwatched episodes despite the integrity error in bulk_create
        self.assertEqual(len(all_episodes) * 2, len(UnwatchedEpisode.objects.all()))

# TEST BELOW NEEDS TO BE REFACTORED
# class FollowedShowsViewTests(TestCase):
#     def setUp(self):
#         self.user = Person.objects.create_user(username='foo', password='bar')
#         self.user.save()
#         create_shows(self.user)

    # def test_followed_shows_view(self):
    #     days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday' 'sunday']
    #     response = self.client.login(username='foo', password='bar')
    #     response = self.client.get(reverse('users:followed'))
    #     self.assertEqual(200, response.status_code)
    #     self.assertTemplateUsed(response, template_name='users/followed.html')
    #     self.assertTrue(response.context['shows'])
    #     shows = response.context['shows']
    #     for show in shows:
    #         # test fails because show.air_days is a string like monday,tuesday, etc
    #         # remove some days and add fixed date to create_shows in setUp method
    #         print(show.air_days)
    #         self.assertTrue(show.air_days in days)
    #
    # def test_follow_shows_with_bad_day(self):
    #     """follow_shows view should return an empty list if no shows air on that day"""
    #     # test broken because no bad day in test atm
    #     day = 'saturday'
    #     response = self.client.login(username='foo', password='bar')
    #     response = self.client.get(reverse('users:followed_day', args=(day,)))
    #
    #     self.assertEqual(200, response.status_code)
    #     self.assertTemplateUsed(response, template_name='users/followed.html')
    #     self.assertFalse(response.context['shows'])
