from django.test import TestCase
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.test import TestCase
from django.core.exceptions import ValidationError
from .forms import (
    UserRegisterForm, UserCreationForm,
)


class UserListViewTest(TestCase):
    def setUp(self):
        num_user = 3

        for user_id in range(num_user):
            test = User.objects.create_user(
                f"test{user_id}",
                f"test{user_id}@info.com",
                f"1234@test{user_id}"
            )
            test.save()

    # login page testing
    def test_index_url(self):
        response = self.client.get(reverse_lazy('account-login'))
        self.assertEqual(response.status_code, 200)

    def test_login_works_with_correct_values(self):
        response = self.client.login(username='test1', password='1234@test1')
        self.assertTrue(response)

    def test_login_fails_with_in_correct_values(self):
        response = self.client.login(username='man', password='1234@test0')
        self.assertFalse(response)

# Registration form checking


class UserRegistrationFormTest(TestCase):

    def setUp(self):
        self.user_register = UserRegisterForm()
        self.user_register2 = UserRegisterForm(
            data={
                'username': 'anyric',
                'email': 'anyric@gmail.com',
                'password1': 'anyric@1234',
                'password2': 'anyric@1234'
            }
        )

    def test_username_field_label(self):
        self.assertFalse(self.user_register.fields['username'].label is None)
        self.assertTrue(
            self.user_register.fields['username'].label == 'Username')

    def test_email_field_label(self):
        self.assertTrue(self.user_register.fields['email'].label is None)
        self.assertFalse(self.user_register.fields['email'].label == 'Email')

  

    def test_form_is_not_valid(self):
        self.assertFalse(self.user_register.is_valid())

class UserCreateViewTest(TestCase):

    def setUp(self):
        self.test = User.objects.create_user(
            "test", "test@info.com", "1234@test")
        self.test.save()

    def test_user_registration_can_be_accessed(self):
        self.client.login(username='test', password='1234@test')
        response = self.client.get(reverse_lazy('account-register'))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'account-register')

    def test_user_registration(self):
        self.client.login(username='test', password='1234@test')
        data = {'username': 'test1', 'email': 'test1@info.com',
                'password1': '1234@test1', 'password2': '1234@test1'}
        response = self.client.post(reverse_lazy('account-register'), data)
        self.assertEqual(response.status_code, 302)

    def test_user_registration_fails_with_invalid_email(self):
        self.client.login(username='test', password='1234@test')
        data = {'username': 'test1', 'email': 'test1info.com',
                'password': '1234@test1'}
        response = self.client.post(reverse_lazy('account-register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'email',
                             'Enter a valid email address.')

class UserEditViewTest(TestCase):
    def setUp(self):
        self.test = User.objects.create_user("test", "test@info.com", "1234@test")
        self.test2 = User.objects.create_user("test2", "test2@info.com", "1234@test2")
       
        self.test.save()
      
        self.test2.save()

    def test_user_edit_can_be_accessed(self):
        self.client.login(username='test', password='1234@test')
        response = self.client.get(reverse_lazy('account-user-edit'))
        self.assertEqual(response.status_code, 302)

    def test_user_profile_edit(self):
      
        self.client.login(username='test', password='1234@test')
        data={'username':'test1','email':'test1@info.com'}
        response = self.client.post(reverse_lazy('account-user-edit'), data)
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response,reverse_lazy('setting'))
    

    def test_user_login_after_edit(self):
      
        self.client.login(username='test', password='1234@test')
        data={'username':'test1','email':'test1@info.com'}
        response = self.client.post(reverse_lazy('account-user-edit'), data)
        self.assertEqual(response.status_code, 302)
        # self.assertRedirects(response,reverse_lazy('setting'))
        self.client.logout()