import unittest
import json
from flask import session
from tests.base import BaseTestCase
from app.models.User import User


class AuthApiTestCase(BaseTestCase):
    """Auth API Tests."""

    def test_non_registered_user_login(self):
        resp = self.client.post('/api/v1/login', data=json.dumps({'name': 'non_user_blabla', 'password': '123456'}))
        self.assertEqual(resp.status_code, 404)

    def test_registered_user_login(self):
        resp = self.client.post('/api/v1/login', data=json.dumps({'name': 'sysop', 'password': 'Passw0rd!'}))
        self.assertEqual(resp.status_code, 200)

        result = json.loads(resp.data.decode('utf-8'))

        self.assertEqual(result['status'], 'success')

        session['current_user'] = result['data']['user']
        self.assertEqual(session['current_user']['name'], 'sysop')

        session['access_token'] = result['data']['access_token']
        self.assertTrue('access_token' in session)

        session['refresh_token'] = result['data']['refresh_token']
        self.assertTrue('refresh_token' in session)

    def test_token_refresh(self):
        self.assertTrue('refresh_token' in session)

        if session.get('refresh_token'):
            headers = {
                'Authorization': 'Bearer {}'.format(session['refresh_token'])
            }
            resp = self.client.post(
                '/api/v1/token/refresh',
                headers=headers
            )
            self.assertEqual(resp.status_code, 200)

            result = json.loads(resp.data.decode('utf-8'))
            self.assertEqual(result['status'], 'success')
            # print(result['data'])
            # print(type(result['data']))
            session['assess_token'] = result['data']['access_token']
            self.assertTrue('assess_token' in session)
            print('access_token: {}, refresh_token: {}'.format(session.get('access_token'),
                                                               session.get('refresh_token')))

    def test_logout_access(self):
        print(session.get('access_token'))
        self.assertTrue('access_token' in session)

        if session.get('access_token'):
            headers = {
                'Authorization': 'Bearer {}'.format(session.get('access_token'))
            }
            resp = self.client.post(
                '/api/v1/logout/access',
                headers=headers
            )
            self.assertEqual(resp.status_code, 200)

    def test_logout_refresh(self):
        self.assertTrue('refresh_token' in session)
        if session.get('refresh_token'):
            headers = {
                'Authorization': 'Bearer {}'.format(session('refresh_token'))
            }
            resp = self.client.post(
                '/api/v1/logout/refresh',
                headers=headers
            )
            self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
