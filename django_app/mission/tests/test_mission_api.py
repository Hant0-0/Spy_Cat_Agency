from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

class TestListMission(APITestCase):

    def setUp(self):
        data={
            "name": "Max",
            "years_of_experience": 3,
            "breed": "Abyssinian",
            "salary": 1200,
        }
        self.cat = self.client.post(reverse("cats-list"), data=data)
        self.cat_id = self.client.post(reverse("cats-list"), data=data).data['id']


    def test_missions_list_post(self):
        data = {
            "cat": self.cat_id,
            "targets": [
                {"name": "Target A", "country": "France", "notes": "initial note"},
                {"name": "Target B", "country": "Germany", "notes": "note 2"}
            ]
        }

        response = self.client.post(reverse("list-missions"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data["targets"][0]["country"] = "None"
        response = self.client.post(reverse("list-missions"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "cat": self.cat_id,
            "targets": [
                {"name": "Target 1", "country": "France", "notes": "initial note"},
                {"name": "Target 2", "country": "Germany", "notes": "note 2"},
            ]
        }
        data["targets"] += [{"name": "Target 3", "country": "Ukraine", "notes": "test 1"},
                            {"name": "Target 4", "country": "Poland", "notes": "test 2"}]
        response = self.client.post(reverse("list-missions"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


        data["targets"] = []
        response = self.client.post(reverse("list-missions"), data=data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_mission_list_get(self):
        response = self.client.get(reverse("list-missions"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestMissionDetail(APITestCase):

    def setUp(self):
        data = {
            "name": "Max",
            "years_of_experience": 3,
            "breed": "Abyssinian",
            "salary": 1200,
        }
        self.cat_id = self.client.post(reverse("cats-list"), data=data).data['id']
        data["name"] = "Bug"
        self.free_cat_id = self.client.post(reverse("cats-list"), data=data).data['id']

        data = {
            "cat": self.cat_id,
            "targets": [
                {"name": "Target A", "country": "France", "notes": "initial note"},
            ]
        }
        self.mission_id = self.client.post(reverse("list-missions"), data=data, format="json").data['id']

        del data["cat"]
        self.mission_id_unassing_cat = self.client.post(reverse("list-missions"), data=data, format="json").data['id']

    def test_mission_detail_get(self):
        response = self.client.get(
            reverse('detail-mission', args=[self.mission_id])
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mission_detail_delete(self):
        response = self.client.delete(
            reverse('detail-mission', args=[self.mission_id])
        )

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_assign_mission(self):
        response = self.client.post(
            reverse('assign-mission', args=[self.mission_id_unassing_cat]), data={"cat": self.cat_id}
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

        response = self.client.post(
            reverse('assign-mission', args=[self.mission_id_unassing_cat]), data={"cat": self.free_cat_id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.post(
            reverse('assign-mission', args=[self.mission_id]), data={"cat": self.free_cat_id}
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)


    def test_unassign_mission(self):
        response = self.client.post(
            reverse('unassign-mission', args=[self.mission_id]), data={"cat": self.cat_id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)



