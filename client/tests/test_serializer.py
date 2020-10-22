from django.test import TestCase
import pytest
from client.models import Company, Department, Employee, EmpProfile
from client.serializers import Company_Serializer, Department_Serializer, Employee_Serializer, EmpProfile_Serializer

class TestCompanySerializer(TestCase):

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
    


class TestDepartmentSerializer(TestCase):

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
    

class TestEmpoyeeSerializer(TestCase):

    @pytest.mark.django_db
    def test_employee_serializer(self):
        comp = Company.objects.create(company_name = 'cybage')

        dept = Department.objects.create(dept_name='RP', in_company=comp)

        emp = Employee.objects.create(
            first_name='abhishek', 
            last_name ='bhujbal', 
            role='MGR', 
            phone = 1452369780, 
            address = 'Nerul'
            )
        
        emp.in_dept.add(dept)

        emp_ser = Employee_Serializer(emp)

        self.assertEqual (emp_ser.data['first_name'], emp.first_name)
        self.assertEqual(emp_ser.data['role'], emp.role)
        self.assertEqual(emp_ser.data['last_name'], emp.last_name)
        self.assertEqual(emp_ser.data['address'], emp.address)
        self.assertEqual(emp_ser.data['phone'], emp.phone)
        self.assertEqual(emp_ser.data['in_dept'], ['RP'] )


class TestEmpProfileSerializer(TestCase):

    @pytest.mark.django_db
    def setUp(self):

        self.company = Company.objects.create(company_name='cybage')

        self.dept = Department(dept_name = 'HR department', in_company = self.company)
        self.dept.save()

        self.emp = Employee.objects.create(
            role ='MGR',
            first_name ='abhishek',
            last_name ='bhujbal',
            address= 'Nerul',
            phone = 1234567890,

            )
        
        self.emp.in_dept.add(self.dept)

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
        self.assertEqual(data['emp']['in_dept'], ['HR department'])

        self.assertEqual(data['image'], '/media/default.jpg')

