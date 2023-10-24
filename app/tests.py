import unittest
import app
import json

class AppTestCase(unittest.TestCase):
    def set_up(self):
        app.app.testing = True
        self.app = app.app.test_client()

    def test_home_endpoint(self):
        response = self.app.get('/')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('Welcome', data)

    def test_valid_user_recommend_route(self):
        user_id = 1  # valid user ID
        response = self.app.get(f'/recommend/{user_id}')
        self.assertEqual(response.status_code, 200)

    def test_invalid_user_recommend_route(self):
        user_id = 9999  # An invalid user ID
        response = self.app.get(f'/recommend/{user_id}')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

