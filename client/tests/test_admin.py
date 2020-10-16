from django.test import TestCase
import pytest
from django.contrib import admin
from django.urls import reverse 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class AdminViewTest(TestCase):
    
    def test_admin_header(self):
        self.assertEqual(admin.site.site_header, "CYBAGE MIS")
    
class SigninTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin@#', email='admin@example.com')
        self.user.save()

    def tearDown(self):
        self.user.delete()

    def test_correct(self):
        user = authenticate(username='admin', password='admin@#')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='test', password='admin@#')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='admin', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)







