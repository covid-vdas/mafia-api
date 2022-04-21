import datetime
import random
from rest_framework import status
from rest_framework.test import APITestCase

ROLE = {
    'admin': '62166447748d2599a7e8d774',
    'manager': '6216644e748d2599a7e8d775',
    'staff': '62166453748d2599a7e8d776'

}


class TestRole(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # connectDB()

    # Case 1: Get all role
    def test_get_all_role(self):
        counter = 0

        res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        role = self.client.get('/api/role/', **header)

        self.assertEqual(role.status_code, status.HTTP_200_OK)

        counter += 1

        print('Pass {} on {}'.format(counter, 1))

    # Case 2: Get role by id
    def test_get_role_by_id(self):
        counter = 0

        res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        role = self.client.get('/api/role/6216644e748d2599a7e8d775' + '/', **header)

        self.assertEqual(role.status_code, status.HTTP_200_OK)

        counter += 1

        print('Pass {} on {}'.format(counter, 1))






