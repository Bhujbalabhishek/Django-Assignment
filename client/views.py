from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Company, Department, Employee, EmpProfile
# Create your views here.


def index(request):
    context = {
    'company' : Company.objects.all(),
    'department' : Department.objects.all(),
    'employee' : EmpProfile.objects.all()
    }
    
    return render(request, 'client/home.html', context)