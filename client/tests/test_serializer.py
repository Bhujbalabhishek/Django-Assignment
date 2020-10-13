from django.test import TestCase
import unittest
import pytest
from client.models import Company, Department, Employee, EmpProfile
from client.serializers import Company_Serializer, Department_Serializer, Employee_Serializer, EmpProfile_Serializer

class TestCompanySerializer(unittest.TestCase):

    @pytest.mark.django_db
    def setUp(self):

        #set of attributes (self.company_attributes) that is use to initialize a Company object
        self.company_attributes = {
            'company_name' : 'cybage'
        }
        #self.serializer_data is also a set of attributes but this time to be used as default data parameters to the serializer when we need them
        self.serializer_data = {
            id: 1,
            'company_name' : 'cybage'
        }

        #creating the company object
        self.company = Company.objects.create(**self.company_attributes)

        #self.serializer which is a simple instance of the serializer initialized with the self.company object.
        self.serializer = Company_Serializer(instance = self.company)

    #verifies if the serializer has the exact attributes it is expected to
    @pytest.mark.django_db
    def test_contains_expected_fields(self):
        data = self.serializer.data

        #usage of set make sure that the output from the serializer has the exact keys
        self.assertEqual(set(data.keys()), set(['id','company_name']))
    

    @pytest.mark.django_db
    def test_company_name_field_content(self):
        data = self.serializer.data

        # checking if the serializer produces the expected data to given field
        self.assertEqual(data['company_name'], self.company_attributes['company_name'])
    


class TestDepartmentSerializer(unittest.TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.company = Company.objects.create(company_name='cybage')

        self.dept_attributes = {
            'dept_name' : 'HR department',
            'in_company' : self.company
        }
        
        self.serializer_data = {
            'id': 1,
            'dept_name' : 'HR department',
            'in_company' : self.company
        }

        self.dept = Department.objects.create(**self.dept_attributes)

        self.serializer = Department_Serializer(instance = self.dept)
    

    @pytest.mark.django_db
    def test_contains_expected_fields(self):

        data = self.serializer.data   
        self.assertEqual(set(data.keys()), set(['id', 'dept_name', 'in_company']))
    


    @pytest.mark.django_db
    def test_dept_field_content(self):
        data = self.serializer.data
    
        # checking if the serializer produces the expected data to given field
        self.assertEqual(data['dept_name'], self.dept_attributes['dept_name'])
        self.assertEqual(data['in_company'], 'cybage')
    

class TestEmpoyeeSerializer(unittest.TestCase):

    @pytest.mark.django_db
    def setUp(self):

        self.company = Company.objects.create(company_name='cybage')
        # self.dept = Department(dept_name = ['HR department', 'IS department'], in_company = self.company)
        # self.dept.save()
        # record = Department.objects.get(id=1)
        self.emp_attributes = {
            'role' : 'MGR',
            'first_name' : 'abhishek',
            'last_name' : 'bhujbal',
            'address': 'Nerul',
            'phone': 1234567890,

        }
        
        self.emp_data = {
            'id': 1,
            'role' : 'MGR',
            'first_name' : 'abhishek',
            'last_name' : 'bhujbal',
            'address': 'Nerul',
            'phone': 1234567890,
            # 'in_dept' : ['HR department', 'IS department']
        }

        self.emp = Employee.objects.create(**self.emp_attributes)

        self.serializer = Employee_Serializer(instance = self.emp)

    @pytest.mark.django_db
    def test_contains_expected_fields(self):

        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['id', 'role', 'first_name', 'last_name', 'address', 'phone', 'in_dept']))


    @pytest.mark.django_db
    def test_emp_field_content(self):
        data = self.serializer.data
    
        # checking if the serializer produces the expected data to given field
        self.assertEqual(data['role'], self.emp_attributes['role'])
        self.assertEqual(data['first_name'], self.emp_attributes['first_name'])
        self.assertEqual(data['last_name'], self.emp_attributes['last_name'])
        self.assertEqual(data['address'], self.emp_attributes['address'])
        self.assertEqual(data['phone'], self.emp_attributes['phone'])
        self.assertEqual(data['in_dept'], [])
    


class TestEmpProfileSerializer(unittest.TestCase):

    @pytest.mark.django_db
    def setUp(self):

        self.company = Company.objects.create(company_name='cybage')

        self.dept = Department(dept_name = ['HR department', 'IS department'], in_company = self.company)
        self.dept.save()

        self.emp = Employee.objects.create(
            role ='MGR',
            first_name ='abhishek',
            last_name ='bhujbal',
            address= 'Nerul',
            phone = 1234567890,

            )

        self.empprof_attributes = {
            'emp': self.emp,
            'image' : 'default.jpg'

        }
        
        self.empprof_data = {
            id: 1,
            'emp': self.emp,
            'image' : 'default.jpg'
        }

        self.empprof = EmpProfile.objects.create(**self.empprof_attributes)

        self.serializer = EmpProfile_Serializer(instance = self.empprof)

    @pytest.mark.django_db
    def test_contains_expected_fields(self):

        data = self.serializer.data

        self.assertEqual(set(data.keys()), set(['id', 'emp', 'image']))


    @pytest.mark.django_db
    def test_empprof_field_content(self):
        data = self.serializer.data
        em = Employee.objects.get(id=1)
        # checking if the serializer produces the expected data to given field
        self.assertEqual(data['emp']['first_name'], em.first_name)
        self.assertEqual(data['emp']['last_name'], em.last_name)
        self.assertEqual(data['emp']['role'], em.role)
        self.assertEqual(data['emp']['address'], em.address)
        self.assertEqual(data['emp']['phone'], em.phone)
        self.assertEqual(data['emp']['in_dept'], [])

        self.assertEqual(data['image'], '/media/default.jpg')

