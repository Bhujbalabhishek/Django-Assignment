from rest_framework import serializers
from client.models import Company, Department, Employee, EmpProfile

class Company_Serializer(serializers.ModelSerializer):

    class Meta:
        model = Company
        fields = ["id", "company_name"]


class Department_Serializer(serializers.ModelSerializer):

    comp =  Company.objects.all()
    in_company = serializers.SlugRelatedField(slug_field='company_name', queryset = comp)
    
    # in_company = serializers.ReadOnlyField(source='in_company.company_name')
    # in_company = Company_Serializer

    class Meta:
        model = Department
        fields = ["id", "dept_name", "in_company"]


class Employee_Serializer(serializers.ModelSerializer):

    dept =  Department.objects.all()
    in_dept = serializers.SlugRelatedField(slug_field='dept_name', queryset=dept, many=True)

    # in_dept = serializers.PrimaryKeyRelatedField(queryset=dept, many=True)
    # in_dept = Department_Serializer(dept, many=True)


    class Meta:
        model = Employee
        fields = ["id", "role", "first_name", "last_name", "address", "phone", "in_dept"]


class EmpProfile_Serializer(serializers.ModelSerializer):

    emp = Employee_Serializer(read_only=True)
    
    class Meta:
        model = EmpProfile
        fields = ["id", "emp", "image"]





