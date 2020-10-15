from django.test import TestCase, Client, RequestFactory
from client.models import Company, Department, Employee, EmpProfile
import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.urls import reverse, NoReverseMatch
from django.db.models.base import ModelBase

class AdminViewTest(TestCase):
    
    def test_admin_header(self):
        self.assertEqual(admin.site.site_header, "CYBAGE MIS")
    

class MockSuperUser:
    def has_perm(self, perm):
        return True


request_factory = RequestFactory()
request = request_factory.get('/admin')
request.user = MockSuperUser()


