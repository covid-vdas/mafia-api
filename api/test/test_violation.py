import datetime
import random
from rest_framework import status
from rest_framework.test import APITestCase

ROLE = {
    'admin': '62166447748d2599a7e8d774',
    'manager': '6216644e748d2599a7e8d775',
    'staff': '62166453748d2599a7e8d776'

}


class TestViolation(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # connectDB()

    # Case 1: Get all camera
    def test_get_all_by_violation(self):
        counter = 0

        res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        violation = self.client.get('/api/violation/', **header)

        self.assertEqual(violation.status_code, status.HTTP_200_OK)

        counter += 1

        print('Pass {} on {}'.format(counter, 1))

    # Case 2: Get camera by id
    def test_get_violation_by_id(self):
        counter = 0

        res = self.client.post('/api/login/', {'username': 'vdas-admin', 'password': '123456@Bc'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        violation = self.client.get('/api/violation/' + '6253184c0671f4fe61cae925/', **header)

        self.assertEqual(violation.status_code, status.HTTP_200_OK)

        counter += 1

        print('Pass {} on {}'.format(counter, 1))






