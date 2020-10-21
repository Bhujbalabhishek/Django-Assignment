from django.test import TestCase
import pytest
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from client.models import Company, Department, Employee, EmpProfile

from django.contrib.admin.sites import AdminSite
from nested_admin import NestedStackedInline, NestedModelAdmin
from client.admin import CompanyAdmin, DepartmentAdmin, EmployeeAdmin
from django.urls import reverse

class SigninTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin@#', email='admin@example.com')
        self.user.save()

    #check whether user type correct username and password
    def test_correct(self):
        user = authenticate(username='admin', password='admin@#')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_not_loggedin(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/admin/login/?next=/admin/')

    def test_loggedin(self):
        login = self.client.login(username='admin', password='admin@#')
        response = self.client.get(reverse('admin:index'))
        
    # checking user is logged in
        self.assertEqual(str(response.context['user']), 'admin')
    # checking "success"
        self.assertEqual(response.status_code, 200)   

    # checking username is false
    def test_wrong_username(self):
        user = authenticate(username='test', password='admin@#')
        self.assertFalse(user is not None and user.is_authenticated)

    # checking password is false
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
    

class MockRequest:
    pass

class MockSuperUser:
    def has_perm(self, perm, obj=None):
        return True

request = MockRequest()
request.user = MockSuperUser()

class ModeladminTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.comp = Company.objects.create(
            company_name = 'cybage'
        )
    
    def setUp(self):
        self.site = AdminSite()
    
    def test_nestedmodeladmin_str(self):
        co = CompanyAdmin(Company, self.site)
        self.assertEqual(str(co), 'client.CompanyAdmin')

    def test_company_admin(self):
        self.assertIsNone(self.site.register(Company, NestedModelAdmin))
    
    def test_default_fields(self):
        co = CompanyAdmin(Company, self.site)
        self.assertEqual(list(co.get_form(request).base_fields), ['company_name'])
        self.assertEqual(list(co.get_fields(request)), ['company_name'])
        self.assertEqual(list(co.get_fields(request, self.comp)), ['company_name'])
        self.assertIsNone(co.get_exclude(request, self.comp))  

    def test_default_fieldsets(self):
        # fieldsets_add and fieldsets_change should return a special data structure that
        # is used in the templates. They should generate the "right thing" whether we
        # have specified a custom form, the fields argument, or nothing at all.
        #
        # Here's the default case. There are no custom form_add/form_change methods,
        # no fields argument, and no fieldsets argument.
        co = CompanyAdmin(Company, self.site)
        self.assertEqual(co.get_fieldsets(request), [(None, {'fields': ['company_name']})])
        self.assertEqual(co.get_fieldsets(request, self.comp), [(None, {'fields': ['company_name']})])   



