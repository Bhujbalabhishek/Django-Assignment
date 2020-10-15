from django.urls import reverse, resolve
from django.test import TestCase

class TestURL(TestCase):

    def test_comp_list_url(self):

        path = reverse('company_list')
        assert resolve(path).view_name == 'company_list'
    
    def test_comp_detail_url(self):

        path = reverse('company_detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'company_detail'
    

    def test_dept_list_url(self):

        path = reverse('dept_list')
        assert resolve(path).view_name == 'dept_list'

    def test_dept_detail_url(self):

        path = reverse('dept_detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'dept_detail'
    
    def test_emp_list_url(self):

        path = reverse('emp_list')
        assert resolve(path).view_name == 'emp_list'

    def test_emp_detail_url(self):

        path = reverse('emp_detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'emp_detail'


    def test_empprof_list_url(self):

        path = reverse('empprof_list')
        assert resolve(path).view_name == 'empprof_list'

    def test_empprof_detail_url(self):

        path = reverse('empprof_detail', kwargs={'pk': 1})
        assert resolve(path).view_name == 'empprof_detail'