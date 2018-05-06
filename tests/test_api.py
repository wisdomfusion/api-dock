import unittest
import json
from app import create_app, db
from app.models import User, Role


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_api_headers(self, name, password):
        return {'token': ''}

    def test_404(self):
        response = self.client.get(
            '/wrong/url',
            headers=self.get_api_headers('name', 'password')
        )
        self.assertEqual(response.status_code, 404)
        json_response = json.loads(response.get_data(as_text=True))
        self.assertEqual(json_response['error'], 'not found')

    def test_no_auth(self):
        response = self.client.get('/api/v1/users', content_type='application/json')
        self.assertEqual(response.status_code, 401)
