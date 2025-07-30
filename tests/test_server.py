import unittest
from server.server import app  # Adjust the import based on your server implementation

class ServerTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/home')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hello from Server', response.data)

    def test_heartbeat(self):
        response = self.app.get('/heartbeat')
        self.assertEqual(response.status_code, 200)

    def test_not_found(self):
        response = self.app.get('/not-an-endpoint')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Endpoint not found', response.data)

    def tearDown(self):
        pass  # Clean up any resources if needed

if __name__ == '__main__':
    unittest.main()