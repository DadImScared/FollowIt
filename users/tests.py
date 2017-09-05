from django.test import TestCase
from .models import Person, FollowedShows

# Create your tests here.


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
