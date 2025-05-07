# Contents of /InfraAuditAI/InfraAuditAI/src/tests/test_main.py

import unittest
from app.main import app

class TestMain(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to InfraAuditAI', response.data)

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'status': 'healthy'})

if __name__ == '__main__':
    unittest.main()