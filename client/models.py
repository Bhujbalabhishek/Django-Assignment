from django.db import models

class Company(models.Model):
    company_name = models.CharField(max_length = 100, blank = False)

    def __str__(self):
        return self.company_name
    
    class Meta:
        verbose_name_plural = "Company" 
        



class Department(models.Model):
    dept_name = models.CharField(max_length = 100, blank = False)
    in_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return ' {} from {}'.format(self.dept_name, self.in_company)

    class Meta:
        verbose_name_plural = "Department"
        



class Employee(models.Model):

    Designation = (
        ('BASE', 'base employee'),
        ('MGR', 'manager'),
        ('SRMGR', 'senior manager'),
        ('PRES', 'president'),
        ('VPRES', 'vice president'),
        ('JRDEV', 'junior developer'),
        ('SRDEV', 'senior developer')
    )

    role = models.CharField(max_length = 50, choices = Designation)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    address = models.TextField()
    phone = models.IntegerField(unique =True)
    in_dept = models.ManyToManyField(Department)

    def __str__(self):
        return f"{self.first_name}{self.last_name}"

    class Meta:
        verbose_name_plural = "Employee"
        

class EmpProfile(models.Model):
    emp = models.OneToOneField(Employee, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.emp.first_name} EmpProfile"

    class Meta:
        verbose_name_plural = "EmpProfile" 

