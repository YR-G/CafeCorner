from django.test import TestCase, Client
from django.urls import reverse
from cafes.models import CafeShop
from users.models import CafeOwner

class CafeTestCase(TestCase):
    def setUp(self):
        """ Set up test data """
        self.client = Client()
        self.owner = CafeOwner.objects.create(
            first_name="Alice", last_name="Smith", email="alice@163.com", password="123456"
        )

        self.cafe1 = CafeShop.objects.create(
            name="Starbucks", owner=self.owner, address="G3 8QP", price_range="£10-20", average_rating=4.5
        )
        self.cafe2 = CafeShop.objects.create(
            name="Costa Coffee", owner=self.owner, address="G4 8NX", price_range="£0-10", average_rating=4.0
        )

        # URLs for different test cases
        self.list_url = reverse("cafes:sorting")  # Get all cafes
        self.detail_url = reverse("cafes:cafe_overview", kwargs={"cafe_id": self.cafe1.id})
        self.sorting_url = reverse("cafes:sorting") + "?filter=rating&order=high-to-low"
        self.search_url = reverse("cafes:search_cafe") + "?query=Starbucks"

    def test_get_cafes(self):
        """ Test retrieving cafe list """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Starbucks")
        self.assertContains(response, "Costa Coffee")

    def test_search_cafe(self):
        """ Test searching for a cafe """
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"success": True, "cafe_id": self.cafe1.id})

    def test_cafe_overview(self):
        """ Test viewing cafe details """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Starbucks")

    def test_sorting(self):
        """ Test sorting cafes by rating """
        response = self.client.get(self.sorting_url, HTTP_X_REQUESTED_WITH="XMLHttpRequest")  # Simulate AJAX request
        self.assertEqual(response.status_code, 200)
        json_data = response.json()
        self.assertGreaterEqual(json_data[0]["average_rating"], json_data[1]["average_rating"])  # Ensure correct sorting
