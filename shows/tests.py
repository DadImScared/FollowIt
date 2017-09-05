from django.test import TestCase
from django.urls import reverse
import json

from users.models import Person

# Create your tests here.


class ToggleFollowingTest(TestCase):
    def setUp(self):
        self.user = Person.objects.create_user(username='foo', password='bar')
        self.user.save()

    def test_toggle_following(self):
        """toggle_following() should follow or un follow a show"""

        response = self.client.login(username='foo', password='bar')

        # follow
        response = self.client.post('/shows/follow/', data={"show": 1})
        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {"following": True})
        self.assertEqual(1, len(self.user.followedshows_set.all()))

        # un follow
        response = self.client.post('/shows/follow/', data={"show": 1})
        self.assertEqual(200, response.status_code)
        self.assertJSONEqual(str(response.content, encoding='utf-8'), {"following": False})
        self.assertFalse(self.user.followedshows_set.all())
