import unittest
from load_balancer.load_balancer import app, hash_ring

class TestLoadBalancer(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        # Reset hash ring for each test
        hash_ring.servers.clear()
        hash_ring.ring = [None] * hash_ring.slots

    def test_add_server(self):
        response = self.client.post('/add', json={"n": 1, "hostnames": ["TestServer"]})
        self.assertEqual(response.status_code, 200)
        self.assertIn("TestServer", response.json["message"]["added"])

    def test_remove_server(self):
        self.client.post('/add', json={"n": 1, "hostnames": ["TestServer"]})
        response = self.client.delete('/rm', json={"n": 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn("TestServer", response.json["message"]["removed"])

    def test_get_replicas(self):
        self.client.post('/add', json={"n": 2, "hostnames": ["S1", "S2"]})
        response = self.client.get('/rep')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["message"]["N"], 2)
        self.assertIn("S1", response.json["message"]["replicas"])
        self.assertIn("S2", response.json["message"]["replicas"])

    def test_home_no_servers(self):
        response = self.client.get('/home?id=123')
        self.assertEqual(response.status_code, 503)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()