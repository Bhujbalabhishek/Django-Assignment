from django.test import TestCase
from client.models import Company, Department, Employee, EmpProfile
import unittest
import pytest

class TestCompany(unittest.TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.comp = Company.objects.create(company_name = "cybage")

    # test for __str__ method
    @pytest.mark.django_db
    def test_str_is_equal_to_company_name(self):
        self.assertEqual(self.comp.company_name, "cybage")

  
class TestDepartment(unittest.TestCase):

    @pytest.mark.django_db
    def test_fields_in_comp_dept_name(self):
        comp = Company(company_name = "cybage")
        comp.save()

        dept = Department(dept_name = "IS", in_company = comp)
        dept.save()

        #fetch the record from department model
        record = Department.objects.get(id=1)

        #test for Department Model fields
        self.assertEqual(record.in_company, comp)
        self.assertEqual(record.dept_name , "IS")

        # test for __str__ method
        self.assertEqual(str(record)," IS from cybage")


class TestEmployee(unittest.TestCase):

    @pytest.mark.django_db
    def test_fields_for_employee(self):
        #creating choices fields
        desig = (

        ('BASE', 'base employee'),
        ('MGR', 'manager'),

            )

        comp = Company(company_name = "cybage")
        comp.save()

        dept2 = Department.objects.create(dept_name = "IS", in_company = comp)
        dept3 = Department.objects.create(dept_name = "HR", in_company = comp)

        record2 = Department.objects.get(id = 1)
        record3 = Department.objects.get(id = 2)

        emp = Employee.objects.create(
            role = desig,
            first_name = "abhishek",
            last_name = "bhujbal",
            address = "Nerul",
            phone = 1234567890
        )

        
        dep = emp.in_dept.create(dept_name = "IS", in_company = comp)
        dep.save()

        # test for __str__ method
        self.assertEqual(str(emp), "abhishekbhujbal")
        
        self.assertEqual(str(record2), " IS from cybage")
        self.assertEqual(str(record3), " HR from cybage")

        #test for choices 
        self.assertEqual(emp.role[0], ('BASE', 'base employee'))
        self.assertEqual(emp.role[1], ('MGR', 'manager'))

        #test for dept in company
        self.assertEqual(dep.dept_name, "IS")
        self.assertEqual(dep.in_company, comp)



class TestEmployeeProfile(unittest.TestCase):

    @pytest.mark.django_db
    def test_field_for_empprofile(value):
        desig = (

        ('BASE', 'base employee'),
        ('MGR', 'manager'),

            )
        employee= Employee.objects.create(
            role = desig,
            first_name = "abhishek",
            last_name = "bhujbal",
            address = "Nerul",
            phone = 1234567890
        )

        comp = Company(company_name = "cybage")
        comp.save()
        
        dep = employee.in_dept.create(dept_name = "IS", in_company = comp )
        dep.save()
        
        #creating a EmployeeProfile Object
        emp_profile = EmpProfile.objects.create(
            emp = employee,
            image = '/media/default.jpg'
            )

        #test for __str__ method
        assert str(emp_profile) == 'abhishek EmpProfile'

        #test for the image path
        assert emp_profile.image == '/media/default.jpg'



    












    # @pytest.fixture
    # def value():
    #     comp = Company(company_name = "cybage")
    #     comp.save()
    #     record = Company.objects.get(id=1)
    #     return record



    # def test_str_is_equal_to_company_name(value):
        
    #     assert value.record.company_name == "cybage"
