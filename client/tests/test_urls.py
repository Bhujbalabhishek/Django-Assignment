from django.urls import reverse, resolve
from django.test import TestCase

class TestURL(TestCase):

    def test_comp_list_url(self):

        path = reverse('company-list')
        assert resolve(path).view_name == 'company-list'
    
    def test_comp_detail_url(self):

        path = reverse('company-detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'company-detail'
    

    def test_dept_list_url(self):

        path = reverse('departments-list', args =(1,))
        assert resolve(path).view_name == 'departments-list'

    def test_dept_detail_url(self):

        path = reverse('departments-detail', args =(1,1,))
        assert resolve(path).view_name == 'departments-detail'
    
    def test_emp_list_url(self):

        path = reverse('employees-list', args=(1,1,))
        assert resolve(path).view_name == 'employees-list'

    def test_emp_detail_url(self):

        path = reverse('employees-detail', args=(1,1,1,))
        assert resolve(path).view_name == 'employees-detail'


    def test_empprof_list_url(self):

        path = reverse('empprofile-list')
        assert resolve(path).view_name == 'empprofile-list'

    def test_empprof_detail_url(self):

        path = reverse('empprofile-detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'empprofile-detail'