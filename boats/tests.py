from rest_framework.test import APITestCase

from accounts.models import User

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
        new_amenity_name = "New Amenity create test"
        new_amenity_desc = "New Amenity desc"
        response = self.client.post(
            self.TEST_URL, data={"name": new_amenity_name, "desc": new_amenity_desc}
        )
        data = response.json()

        self.assertEqual(response.status_code, 200, "Status is not 200")
        self.assertEqual(data["name"], new_amenity_name, "name is not same")
        self.assertEqual(data["desc"], new_amenity_desc, "desc is not same")
        self.assertIn("name", data, "name is not find")


"""
class TestAmenity(APITestCase):
    TEST_NAME = "TestAmenity name"
    TEST_DESC = "TestAmenity desc"

    def setUp(self):
        models.Amenity.objects.create(
            name=self.TEST_NAME,
            desc=self.TEST_DESC,
        )
        return super().setUp()

    def test_amenity_not_found(self):
        response = self.client.get("/api/v1/boats/amenities/2")
        self.assertEqual(response.status_code, 404)

    def test_get_amenity(self):
        response = self.client.get("/api/v1/boats/amenities/1")
        self.assertEqual(response.status_code, 200)

        data = response.json()

        self.assertEqual(
            data["name"],
            self.TEST_NAME,
        )
        self.assertEqual(
            data["desc"],
            self.TEST_DESC,
        )

    def test_put_amenity(self):
        # code challenge
        # 경우 1 : Serializer가 유효해서 유저가 Amenity 업데이트를 할 수 있는 경우
        # 경우 2 : Serializer가 유효하지 않은 경우

        pass
    

    def test_delete_amenity(self):
        response = self.client.delete("/api/v1/boats/amenities/1")
        self.assertEqual(response.status_code, 204)
"""


class TestBoats(APITestCase):
    # self.assert (must)
    def setUp(self):
        test_user = User.objects.create(
            username="test",
        )
        test_user.set_password("123")
        test_user.save()

        self.user = test_user

    def test_create_boat(self):
        response = self.client.post("/api/v1/boats/")
        print(response)

        self.client.force_login(self.user)

        response = self.client.post("/api/v1/boats/")
        print(response.json())
