import datetime
import random
from rest_framework import status
from rest_framework.test import APITestCase

ROLE = {
    'admin': '62166447748d2599a7e8d774',
    'manager': '6216644e748d2599a7e8d775',
    'staff': '62166453748d2599a7e8d776'

}


class TestArea(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # connectDB()

    # Case 1: Get all camera
    def test_get_all_area(self):
        counter = 0

        res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        users = self.client.get('/api/area/', **header)

        self.assertEqual(users.status_code, status.HTTP_200_OK)

        counter += 1

        print('Pass {} on {}'.format(counter, 1))

    # Case 2: Get all area

    def test_get_all_area(self):
        counter = 0

        res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        users = self.client.get('/api/area/?page=2&limit=10', **header)

        self.assertEqual(users.status_code, status.HTTP_200_OK)

        counter += 1

        print('Pass {} on {}'.format(counter, 1))

    # Case 3: Get area by id
    def test_get_area_by_id(self):
        counter = 0

        res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        camera = self.client.get('/api/area/' + '62176393052ab85305e21f8b/', **header)

        self.assertEqual(camera.status_code, status.HTTP_200_OK)

        counter += 1

        print('Pass {} on {}'.format(counter, 1))

    # Case 4:Add new area
    def test_add_new_area(self):
        counter = 0
        list_areas = [
            {
                'name': 'cam trong ngo 123',
                'managed_manager': '6252e9ece5dc20954d5d2e46'
            },
            {
                'name': 'cam ngoai hem 155',
                'managed_manager': '6252e9ece5dc20954d5d2e46'
            },
            {
                'name': 'cam tren duong',
                'managed_manager': '6252e9ece5dc20954d5d2e46'

            },

        ]
        for area in list_areas:
            print(area)
            counter += 1
            res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

            token = res.data['token']
            header = {
                'HTTP_AUTHORIZATION': f'Bearer {token}'
            }
            users = self.client.post('/api/area/', area, **header)

            self.assertEqual(users.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_areas)))

    # Case 54: Test edit camera by id
    def test_edit_area(self):
        counter = 0
        list_area = [
            {
                'name': 'cam trong ngo 999',

            },
            {
                'url': '99.33.42.55',
            },
            {
                'area_id': '621763a5052ab85305e21f8d'
            },

        ]
        for area in list_area:
            print(area)
            counter += 1
            res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

            token = res.data['token']
            header = {
                'HTTP_AUTHORIZATION': f'Bearer {token}'
            }
            users = self.client.patch('/api/area/625f7849179761b8c6128cbe/', area, **header)

            self.assertEqual(users.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_area)))

    # Case 6: Delete camera by id
    def test_delete_by_area_id(self):
        counter = 0
        res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        users = self.client.delete('/api/area/' + '62517882cdba35b0a9b8e02e/', **header)

        self.assertEqual(users.status_code, status.HTTP_200_OK)



