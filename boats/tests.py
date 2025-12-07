from rest_framework.test import APITestCase

from . import models


class TestAmenities(APITestCase):
    TEST_NAME = "Amenity Test"
    TEST_DESC = "Test Database"
    TEST_URL = "/api/v1/boats/amenities/"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.TEST_NAME,
            desc=self.TEST_DESC,
        )
        return super().setUp()

    def test_all_amenities(self):
        response = self.client.get(self.TEST_URL)
        data = response.json()
        self.assertEqual(
            response.status_code,
            200,
            "status is not 200",
        )
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["name"], self.TEST_NAME)
        self.assertEqual(data[0]["desc"], self.TEST_DESC)

    def test_create_amenity(self):
        response = self.client.post(
            self.TEST_URL, data={"name": "New Amenity create test", "desc": "New Amenity desc"}
        )
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status is not 200")
