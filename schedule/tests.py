
from django.urls import reverse
from django.test import TestCase

# Create your tests here.


class ScheduleViewTests(TestCase):

    def test_schedule_view(self):
        """Schedule with a proper date should return a list of episodes"""
        response = self.client.get(reverse('schedule:schedules'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'schedule/schedules.html')
        self.assertTrue(response.context['schedule'])


class ScheduleViewWithDateTests(TestCase):

    def test_schedule_with_date_view(self):
        """Schedule with any correct date not in the future should return a list of episodes"""
        url = reverse('schedule:schedules_by_date', args=('2014-08-10',))
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'schedule/schedules.html')
        self.assertTrue(response.context['schedule'])
