from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class TestCatViewCase(APITestCase):

    def setUp(self):
        data={
            "name": "Max",
            "years_of_experience": 3,
            "breed": "Abyssinian",
            "salary": 1200,
        }
        self.cat = self.client.post(reverse("cats-list"), data=data)
        self.cat_id = self.cat.data['id']

    def test_cats_list(self):
        response=self.client.get(reverse("cats-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cats_create(self):
        data={
            "name": "Felix",
            "years_of_experience": 1,
            "breed": "Simple",
            "salary": 1000,
        }
        response = self.client.post(reverse("cats-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data["breed"] = "Abyssinian"
        response = self.client.post(reverse("cats-list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_cat_detail_get(self):
        response = self.client.get(reverse('cat-detail', args=[self.cat_id]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('id'), self.cat_id)

    def test_cat_detail_patch(self):
        response = self.client.patch(reverse('cat-detail', args=[self.cat_id]),
                                     data={"name": "Oliver", "salary": 1500})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('name'), self.cat.data['name'])
        self.assertNotEqual(response.data.get('salary'), self.cat.data['salary'])

    def test_cat_detail_delete(self):

        response = self.client.delete(reverse('cat-detail', args=[self.cat_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
