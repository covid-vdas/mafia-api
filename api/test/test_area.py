import datetime
import random
from rest_framework import status
from rest_framework.test import APITestCase

ROLE = {
    'admin': '62166447748d2599a7e8d774',
    'manager': '6216644e748d2599a7e8d775',
    'staff': '62166453748d2599a7e8d776'

}


class TestCamera(APITestCase):

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

    # Case 2: Get all camera pagination

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

    # Case 2: Get camera by id
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

    # Case 3:Add new camera
    def test_add_new_camera(self):
        counter = 0
        list_camera = [
            {
                'name': 'cam trong ngo 123',
                'url': '12345678',
                'area_id': '62176393052ab85305e21f8b'
            },
            {
                'name': 'cam ngoai hem 155',
                'url': '12345678',
                'area_id': '62176393052ab85305e21f8b'
            },
            {
                'name': 'cam tren duong',
                'url': '12345678',
                'area_id': '62517882cdba35b0a9b8e02e'
            },

        ]
        for camera in list_camera:
            print(camera)
            counter += 1
            res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

            token = res.data['token']
            header = {
                'HTTP_AUTHORIZATION': f'Bearer {token}'
            }
            users = self.client.post('/api/camera/', camera, **header)

            self.assertEqual(users.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_camera)))

    # Case 4: Test edit camera by id
    def test_edit_camera(self):
        counter = 0
        list_camera = [
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
        for camera in list_camera:
            print(camera)
            counter += 1
            res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

            token = res.data['token']
            header = {
                'HTTP_AUTHORIZATION': f'Bearer {token}'
            }
            users = self.client.patch('/api/camera/625f7849179761b8c6128cbe/', camera, **header)

            self.assertEqual(users.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_camera)))

    # Case 5: Delete camera by id
    def test_delete_by_camera_id(self):
        counter = 0
        res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        users = self.client.delete('/api/camera/' + '625f7849179761b8c6128cbe/', **header)

        self.assertEqual(users.status_code, status.HTTP_200_OK)

    # Case 6: Test get all camera by id of area
    def test_get_all_camera_by_id_area(self):
        counter = 0
        list_area = [
            {
                'id': '62176393052ab85305e21f8b',

            },
            {
                'id': '6217639a052ab85305e21f8c',
            },
            {
                'id': '621763a5052ab85305e21f8d'
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
            users = self.client.get('/api/camera/getAllCamera/' + area['id'] + '/', **header)

            self.assertEqual(users.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_area)))

