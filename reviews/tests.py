from django.test import TestCase, Client
from django.urls import reverse
from reviews.models import Review
from cafes.models import CafeShop
from users.models import CafeOwner, Customer
from rest_framework import status

class ReviewTestCase(TestCase):
    def setUp(self):
        """ Set up test data """
        self.client = Client()
        self.owner = CafeOwner.objects.create(first_name="Alice", last_name="Smith", email="alice@163.com", password="123456")
        self.customer = Customer.objects.create(first_name="John", last_name="Doe", email="john@163.com", password="123456")
        self.cafe = CafeShop.objects.create(name="Starbucks", owner=self.owner, address="G3 8QP", price_range="£10-20", average_rating=4.5)
        self.submit_review_url = reverse("reviews:get_reviews", kwargs={"cafe_id": self.cafe.id})

        # Set up session to simulate user login
        session = self.client.session
        session["user_id"] = self.customer.id
        session.save()

    def test_create_review(self):
        """ Test Review model """
        review = Review.objects.create(cafe=self.cafe, customer=self.customer, rating=5, comment="Great coffee!")
        self.assertEqual(review.rating, 5) # Check if the rating is correctly stored

    def test_submit_review(self):
        """ Test submitting a review via the API  """
        data = {"rating": 5, "comment": "Amazing coffee!"}
        response = self.client.post(self.submit_review_url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # Ensure that after submitting, the response redirects (HTTP 302)

    def test_review_requires_login(self):
        """ Test that unauthenticated users cannot submit a review """
        self.client.session.flush()  # Clear session to simulate a logged-out user
        data = {"rating": 5, "comment": "Great!"}
        response = self.client.post(self.submit_review_url, data)

        # Ensure unauthenticated users are redirected to the login page
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertTrue("/users/login/" in response.url)

