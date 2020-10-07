from django.test import TestCase
from client.models import Company, Department, Employee, EmpProfile


class TestCompany(TestCase):

    def setUp(self):
        self.comp = Company.objects.create(company_name = "cybage")
        self.comp1 = Company.objects.create(company_name = " ")

    def test_str_is_equal_to_company_name(self):
        self.assertEqual(self.comp.company_name, "cybage" )

    def test_str_is__for_company_name_blank(self):
        self.assertEqual(self.comp1.company_name, " ")   


class TestDepartment(TestCase):
    
    def test_fields_in_comp_dept_name(self):
        comp = Company(company_name = "cybage")
        comp.save()

        dept = Department(dept_name = "IS", in_company = comp)
        dept.save()

        record = Department.objects.get(id=1)

        self.assertEqual(record.in_company, comp)
        self.assertEqual(record.dept_name , "IS")

    def test_str_for_dept_in_comp(self):
        comp = Company.objects.create(company_name = "cybage")
    
        dept = Department.objects.create(dept_name = "IS", in_company = comp)

        record = Department.objects.get(id = 1)
        self.assertEqual(str(record)," IS from cybage")


class TestEmployee(TestCase):


    def test_fields_for_employee(self):

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

        self.assertEqual(str(emp), "abhishekbhujbal")

        self.assertEqual(str(record2), " IS from cybage")
        self.assertEqual(str(record3), " HR from cybage")

        self.assertEqual(emp.role[0], ('BASE', 'base employee'))
        self.assertEqual(emp.role[1], ('MGR', 'manager'))

        self.assertEqual(dep.dept_name, "IS")
        self.assertEqual(dep.in_company, comp)



class TestEmployeeProfile(TestCase):

    def test_field_for_empprofile(self):
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
        
        dep = employee.in_dept.create(dept_name = "IS", in_company = comp)
        dep.save()
        
        emp_profile = EmpProfile.objects.create(
            emp = employee,
            image = 
            )

        self.assertEqual(str(emp_profile), 'abhishek EmpProfile')


    



