from django.test import TestCase, Client
from django.urls import reverse
from users.models import Customer, CafeOwner, Administrator

class UserTestCase(TestCase):
    def setUp(self):
        """ Set up test data """
        self.client = Client()
        self.register_url = reverse("users:register")
        self.login_url = reverse("users:login")

        # Create test users
        self.customer = Customer.objects.create(
            first_name="John", last_name="Doe", email="john@163.com", password="123456"
        )
        self.owner = CafeOwner.objects.create(
            first_name="Alice", last_name="Smith", email="alice@163.com", password="123456"
        )
        self.admin = Administrator.objects.create(
            first_name="Admin", last_name="User", email="admin@163.com", password="123456"
        )

    def test_create_customer(self):
        """ Test Customer model """
        self.assertEqual(self.customer.email, "john@163.com")

    def test_register_user(self):
        """ Test user registration """
        response = self.client.post(self.register_url, {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@123.com",
            "password": "123456",
            "confirm_password": "123456",
            "user_type": "customer"
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after successful registration

    def test_login_user(self):
        """ Test user login """
        response = self.client.post(self.login_url, {
            "email": "john@163.com",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 200)  # Expect a 200 status code after successful login
