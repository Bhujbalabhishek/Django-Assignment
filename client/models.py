from django.db import models
from django.utils.safestring import mark_safe

class Company(models.Model):
    company_name = models.CharField(max_length = 100)

    def __str__(self):
        return self.company_name
    
    
class Department(models.Model):
    dept_name = models.CharField(max_length = 100)
    in_company = models.ForeignKey(Company, on_delete=models.CASCADE)
    
    def __str__(self):
        return ' {} from {}'.format(self.dept_name, self.in_company)


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


class EmpProfile(models.Model):
    emp = models.OneToOneField(Employee, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f"{self.emp.first_name} EmpProfile"
    
    def image_tag(self):
        return mark_safe('<img src = "{}" width="150" />'.format(self.image.url))
    image_tag.short_description = 'Image'
    image_tag.allow_tags = True


