from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TestTargetDetail(APITestCase):

    def setUp(self):
        data = {
            "name": "Max",
            "years_of_experience": 3,
            "breed": "Abyssinian",
            "salary": 1200,
        }
        self.cat_id = self.client.post(reverse("cats-list"), data=data).data['id']

        data = {
            "cat": self.cat_id,
            "targets": [
                {"name": "Target A", "country": "France", "notes": "initial note"},
            ]
        }
        self.mission_id = self.client.post(reverse("list-missions"), data=data, format="json").data['id']

    def test_target_detail_get(self):
        response = self.client.get(
            reverse('detail-target', args=[self.mission_id, 1])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_target_update_notes(self):
        response = self.client.patch(
            reverse('detail-target', args=[self.mission_id, 1]),
            data={"notes": "Test notes"}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse('complete-target', args=[self.mission_id, 1]),
        )
        response = self.client.patch(
            reverse('detail-target', args=[self.mission_id, 1]),
            data={"notes": "Test notes"}
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


    def test_target_complete(self):
        response = self.client.post(
            reverse('complete-target', args=[self.mission_id, 1]),
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)