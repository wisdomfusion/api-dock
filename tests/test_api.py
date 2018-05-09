import unittest
from tests.base import BaseTestCase


class ApiTestCase(BaseTestCase):
    def test_404(self):
        response = self.client.get('/wrong/url')
        self.assertEqual(response.status_code, 404)

    def test_no_auth(self):
        response = self.client.get('/api/v1/users', content_type='application/json')
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
