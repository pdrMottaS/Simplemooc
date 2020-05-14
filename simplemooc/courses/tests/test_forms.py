from django.test import TestCase
from django.core import mail
from django.test.client import Client
from django.urls import reverse
from simplemooc.courses.models import Course
from django.conf import settings

class ContactCourseTest(TestCase):
    def setUp(self):
        self.course=Course.objects.create(name='Django', slug='Django')

    def tearDown(self):
        self.course.delete()
    
    def test_contact_form_error(self):
        data={'name':'fulano', 'email':'', 'message':''}
        client=Client()
        path=reverse('courses:details', args=[self.course.slug])
        response=client.post(path, data)
        self.assertFormError(response, 'form', 'email', 'Este campo é obrigatório.')
        self.assertFormError(response, 'form', 'message', 'Este campo é obrigatório.')
    
    def test_contact_form_success(self):
        data={'name':'fulano', 'email':'fulano@email.com', 'message':'Olá'}
        client=Client()
        path=reverse('courses:details', args=[self.course.slug])
        response=client.post(path, data)
        self.assertEqual(len(mail.outbox),1)
        self.assertEqual(mail.outbox[0].to, [settings.CONTACT_EMAIL])
