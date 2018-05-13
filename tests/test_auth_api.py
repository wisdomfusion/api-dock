import unittest
import json
from tests.base import BaseTestCase
from tests import user_login


class AuthApiTestCase(BaseTestCase):
    """Auth API Tests."""
    def test_non_registered_user_login(self):
        resp = user_login(self, 'non_user_blabla', 'password')
        self.assertEqual(resp.status_code, 404)

    def test_registered_user_login(self):
        resp = user_login(self, 'sysop', 'Passw0rd!')
        self.assertEqual(resp.status_code, 200)

        result = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(result['status'], 'success')
        self.assertTrue(result['data']['user'] is not None)
        self.assertTrue(result['data']['access_token'] is not None)
        self.assertTrue(result['data']['refresh_token'] is not None)

    def test_token_refresh(self):
        resp_login = user_login(self, 'sysop', 'Passw0rd!')
        self.assertEqual(resp_login.status_code, 200)

        result = json.loads(resp_login.data.decode('utf-8'))
        self.assertTrue(result['data']['refresh_token'] is not None)

        headers = {'Authorization': 'Bearer {}'.format(result['data']['refresh_token'])}
        resp = self.client.post('/api/v1/token/refresh', headers=headers)
        self.assertEqual(resp.status_code, 200)

        res = json.loads(resp.data.decode('utf-8'))
        self.assertEqual(res['status'], 'success')
        self.assertTrue(res['data']['access_token'] is not None)

    def test_logout_access(self):
        resp_login = user_login(self, 'sysop', 'Passw0rd!')
        self.assertEqual(resp_login.status_code, 200)

        result = json.loads(resp_login.data.decode('utf-8'))
        self.assertTrue(result['data']['access_token'] is not None)

        headers = {'Authorization': 'Bearer {}'.format(result['data']['access_token'])}
        resp = self.client.post('/api/v1/logout/access', headers=headers)
        self.assertEqual(resp.status_code, 200)

    def test_logout_refresh(self):
        resp_login = user_login(self, 'sysop', 'Passw0rd!')
        self.assertEqual(resp_login.status_code, 200)

        result = json.loads(resp_login.data.decode('utf-8'))
        self.assertTrue(result['data']['access_token'] is not None)

        headers = {'Authorization': 'Bearer {}'.format(result['data']['refresh_token'])}
        resp = self.client.post('/api/v1/logout/refresh', headers=headers)
        self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
