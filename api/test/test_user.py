import datetime
import random
from rest_framework import status
from rest_framework.test import APITestCase

ROLE = {
    'admin': '62166447748d2599a7e8d774',
    'manager': '6216644e748d2599a7e8d775',
    'staff': '62166453748d2599a7e8d776'

}


class TestUser(APITestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # connectDB()

    # Case 1: Verify the login of user
    def test_login_will_successful(self):
        counter = 0
        list_user = [
            {
                'username': 'liti123',
                'password': '12345678'
            },
            {
                'username': 'quanghuy',
                'password': '123456@Bc'
            },
            {
                'username': 'toidaidot123',
                'password': '12345678'
            }
        ]
        for user in list_user:
            print(user)
            counter += 1
            res = self.client.post('/api/login/', user, format="json")
            self.assertEqual(res.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_user)))

    # Case 2: Login failed with invalid user
    def test_login_will_fail(self):
        list_user = [
            {
                'username': 'liti1235',
                'password': '12345678'
            },
            {
                'username': 'quanghuy',
                'password': '123456'
            },
            {
                'username': 'toidaidot123',
                'password': '!@#59dad'
            }
        ]
        counter = 0
        for user in list_user:
            print(user)
            counter += 1
            res = self.client.post('/api/login/', user, format="json")
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        print('Pass {} on {}'.format(counter, len(list_user)))

    # Case 3: Login failed with invalid password
    def test_login_will_fail_with_invalid_user(self):
        list_user = [
            {
                'username': 'liti1235',
                'password': '12345678'
            },
            {
                'username': 'quanghuyy',
                'password': '123456@Bc'
            },
            {
                'username': 'toidaidot11',
                'password': '12345678'
            }
        ]
        counter = 0
        for user in list_user:
            print(user)
            counter += 1
            res = self.client.post('/api/login/', user, format="json")
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        print('Pass {} on {}'.format(counter, len(list_user)))

    # Case 4: Login failed with invalid user and invalid password
    def test_login_will_fail_with_invalid_password(self):
        list_user = [
            {
                'username': 'liti123',
                'password': '12345678@a'
            },
            {
                'username': 'quanghuy',
                'password': '1'
            },
            {
                'username': 'toidaidot123',
                'password': '9999aBc'
            }
        ]
        counter = 0
        for user in list_user:
            print(user)
            counter += 1
            res = self.client.post('/api/login/', user, format="json")
            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

        print('Pass {} on {}'.format(counter, len(list_user)))

    # Case 5: Get all user
    def test_get_all_user(self):
        counter = 0
        list_user = [
            {
                'username': 'asdfg988',
                'password': '12345678'
            },
            {
                'username': 'quanghuy',
                'password': '123456@Bc'
            },
            {
                'username': 'toidaidot123',
                'password': '12345678'
            }
        ]
        for user in list_user:
            print(user)
            counter += 1
            res = self.client.post('/api/login/', user, format="json")

            token = res.data['token']
            header = {
                'HTTP_AUTHORIZATION': f'Bearer {token}'
            }
            users = self.client.get('/api/user/', **header)

            self.assertEqual(users.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_user)))

    # Case 6: Get User by id
    def test_get_user_by_id(self):
        counter = 0
        list_user = [
            {
                'username': 'asdfg988',
                'password': '12345678'
            },
            {
                'username': 'quanghuy',
                'password': '123456@Bc'
            },
            {
                'username': 'toidaidot123',
                'password': '12345678'
            }
        ]
        for user in list_user:
            print(user)
            counter += 1
            res = self.client.post('/api/login/', user, format="json")

            token = res.data['token']
            header = {
                'HTTP_AUTHORIZATION': f'Bearer {token}'
            }
            users = self.client.get('/api/user/' + '622f3433594cefcc4d28712e/', **header)

            self.assertEqual(users.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_user)))

    # Case 7: Create new user
    def test_create_user(self):
        counter = 0
        list_user = [
            {
                'username': 'asdfg988',
                'password': '12345678'
            },
            {
                'username': 'quanghuy',
                'password': '123456@Bc'
            },
            {
                'username': 'toidaidot123',
                'password': '12345678'
            }
        ]
        for user in list_user:
            print(user)
            counter += 1
            res = self.client.post('/api/login/', user, format="json")

            token = res.data['token']
            header = {
                'HTTP_AUTHORIZATION': f'Bearer {token}'
            }

            data = {
                'username': 'fake_data' + str(datetime.datetime.utcnow()),
                'password': datetime.datetime.utcnow(),
                'phone': '0'.join([str(random.randint(1, 10)) for _ in range(0, 9)]),
                'email': 'fake-email'+ str(random.randint(1,100000000)) + '@gmail.com',
                'address': 'fake address ' + str(random.randint(1, 10000)),
                'fullname': 'fake-name '+ str(random.randint(1, 10000000)),
                'birthdate': '2000-12-23'
            }

            users = self.client.post('/api/user/', data=data, format='json', **header)
            print(users.data)
            self.assertEqual(users.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_user)))

    # Case 8: Update partial information user
    def test_update_partial_by_id(self):
        counter = 0
        list_user = [
            {
                'username': 'asdfg988',
                'password': '12345678'
            },
            {
                'username': 'quanghuy',
                'password': '123456@Bc'
            },
            {
                'username': 'toidaidot123',
                'password': '12345678'
            }
        ]
        for user in list_user:
            print(user)
            counter += 1
            res = self.client.post('/api/login/', user, format="json")

            token = res.data['token']
            header = {
                'HTTP_AUTHORIZATION': f'Bearer {token}'
            }
            users = self.client.patch('/api/user/' + '622f3433594cefcc4d28712e/', data={'phone': '035932984'}, **header)

            self.assertEqual(users.status_code, status.HTTP_200_OK)

        print('Pass {} on {}'.format(counter, len(list_user)))

    # Case 9: Delete user
    def test_delete_by_id(self):
        counter = 0
        res = self.client.post('/api/login/', {'username': 'toidaidot123', 'password': '12345678'}, format="json")

        token = res.data['token']
        header = {
            'HTTP_AUTHORIZATION': f'Bearer {token}'
        }
        users = self.client.delete('/api/user/' + '624eb19c70ddf85b0b493051/', data={'phone': '035932984'}, **header)

        self.assertEqual(users.status_code, status.HTTP_200_OK)


