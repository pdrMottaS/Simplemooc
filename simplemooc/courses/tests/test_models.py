from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.urls import reverse
from simplemooc.courses.models import Course
from django.conf import settings
from model_mommy import mommy

class CourseManagerTest(TestCase):
    def setUp(self):
        self.courses_django=mommy.make('courses.Course', name='Django na web',_quantity=5)
        self.courses_devs=mommy.make('courses.Course', name='python para devs',_quantity=10)
        self.client=Client()
    
    def tearDown(self):
        Course.objects.all().delete()
    
    def test_course_serach(self):
        search=Course.objects.search('django')
        self.assertEqual(len(search), 5)
        search=Course.objects.search('python')
        self.assertEqual(len(search), 10)