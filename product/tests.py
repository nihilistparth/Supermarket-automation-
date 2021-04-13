from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
# from models import Transaction
# Create your tests here.
class PurchaseCreationViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        # self.role = Role.objects.create(name="Manager", description="This is a manager role")
        self.test.save()
        # self.role.save()
        self.data = {
            'name': 'sugar',
            'quantity': 10,
            'cost_price': 3000.0,
            'selling_price':3005.0 
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_purchase_list_can_be_accessed(self):
        
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse_lazy('product-transaction'))
        self.assertEqual(response.status_code, 200)
    

    def test_purchase_creation(self):
        
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('product-transaction'))
        self.assertEqual(response.status_code, 200)

    # def test_purchase_count(self):
        
    #     self.client.login(username=self.username, password=self.password)
    #     self.client.post(reverse_lazy('product-transaction'))
    #     count = Transaction.objects.count()
    #     self.assertEqual(count, 1)

    def test_purchase_creation_with_no_login(self):
        
        response = self.client.post(reverse_lazy('product-transaction'), data=self.data)
        self.assertEqual(response.status_code, 302)

    def test_purchase_creation_by_get(self):
        
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('product-transaction'))
        self.assertEqual(response.status_code, 200)

class PurchaseEditViewTest(TestCase):
    def setUp(self):
        test = User.objects.create_user("test", "test@info.com", "1234@test")
        # self.role = Role.objects.create(name="Manager", description="This is a manager role")
        test.save()
        # self.role.save()
        # test.groups.add(Group.objects.get(name='Manager'))
        # self.purch = Purchase.objects.create('name': 'sugar',
        #     'quantity': 10,
        #     'cost_price': 3000.0,
        #     'selling_price':3005.0 ))
        self.data = {
            'name': 'sugar',
            'quantity': 10,
            'cost_price': 3000.0,
            'selling_price':3005.0 
        }
        self.username = 'test'
        self.password = '1234@test'

    def test_edit_purchase_can_be_accessed(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('product-transaction'))
        self.assertEqual(response.status_code, 200)
        

    def test_edit_purchase(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('product-transaction'))
        self.assertEqual(response.status_code, 200)

    def test_edit_purchase_by_get(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse_lazy('product-transaction'))
        self.assertEqual(response.status_code, 200)
