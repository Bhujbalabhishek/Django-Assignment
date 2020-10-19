from django.test import TestCase
import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from client.models import Company, Department, Employee, EmpProfile

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


class AdminViewTest(TestCase):
    
    def test_admin_header(self):
        self.assertEqual(admin.site.site_header, "CYBAGE MIS")
    
    def test_companyhascharfield(self):

        self.comp = Company.objects.create(company_name = 'cybage')

        self.assertEqual(self.comp.company_name,'cybage')
        self.assertNotEqual(self.comp.company_name,123)

    def test_depthascharfield(self):
        self.comp = Company.objects.create(company_name = 'cybage')
        self.dept = Department.objects.create(dept_name = 'HR dept',in_company=self.comp)

        self.assertEqual(self.dept.dept_name,'HR dept')
        self.assertNotEqual(self.dept.dept_name,123)

    def test_employeephoneunique(self):
        self.comp = Company.objects.create(company_name = 'cybage')
        self.dept = Department.objects.create(dept_name = 'HR dept',in_company=self.comp)


        desig = (
            ('BASE', 'base employee'),
            ('MGR', 'manager')
        )

        self.emp1 = Employee.objects.create(
            role = desig,
            first_name = "abhishek",
            last_name = "bhujbal",
            address = "Nerul",
            phone = 1234567890
        )

        self.emp2 = Employee.objects.create(
            role = desig,
            first_name = "demo",
            last_name = "test",
            address = "Nerul",
            phone = 1234567891
        )

        self.assertNotEqual(self.emp1.phone, self.emp2.phone)


    def test_imagefieldofempprof(self):
        desig = (
            ('BASE', 'base employee'),
            ('MGR', 'manager')
        )

        self.emp = Employee.objects.create(
            role = desig,
            first_name = "abhishek",
            last_name = "bhujbal",
            address = "Nerul",
            phone = 1234567890
        )
        
        self.emp_profile = EmpProfile.objects.create(
            emp = self.emp,
            image = '/media/abc.jpg'
            )

        self.assertEqual(EmpProfile.objects.count(), 1)