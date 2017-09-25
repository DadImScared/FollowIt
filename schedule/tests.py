
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth.models import User

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait

from users.models import FollowedShows

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
        self.assertEqual('2014-08-09', response.context['prev_day'])
        self.assertEqual('2014-08-11', response.context['next_day'])
        self.assertEqual('2014-08-03', response.context['prev_week'])
        self.assertEqual('2014-08-17', response.context['next_week'])

    def test_schedule_with_bad_date(self):
        """Schedule with bad date should return 404"""
        url = reverse('schedule:schedules_by_date', args=('2010-80-40',))
        response = self.client.get(url)
        self.assertEqual(404, response.status_code)


class ScheduleViewSeleniumTests(StaticLiveServerTestCase):

    def setUp(self):
        self.user = User.objects.create_user('tom', 'test@test.com', 'password')
        self.client.login(username=self.user.username, password='password')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.refresh()
        cls.selenium.quit()
        super().tearDownClass()

    def tearDown(self):
        self.selenium.refresh()

    def test_follow_show(self):
        """When following a show the shows button should get 'btn-success' class and text should change to Following
        """
        self.assertFalse(FollowedShows.objects.filter(user=self.user))
        timeout = 10
        self.selenium.get('{}/schedule/'.format(self.live_server_url))
        self.selenium.add_cookie({'name': 'sessionid', 'value': self.client.cookies['sessionid'].value, 'secure': False, 'path': '/'})
        self.selenium.refresh()
        self.selenium.get("{}/schedule/".format(self.live_server_url))
        elements = self.selenium.find_elements_by_class_name('follow-btn')
        first_ele = elements[0]
        self.assertTrue('btn-primary' in first_ele.get_attribute('class'))
        self.assertEqual(first_ele.text, 'Follow')
        first_ele.click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_elements_by_class_name('follow-btn')[0].text == 'Following'
        )
        self.assertTrue('btn-success' in first_ele.get_attribute('class'))
        self.assertEqual(first_ele.text, 'Following')
        self.assertTrue(FollowedShows.objects.filter(user=self.user))
