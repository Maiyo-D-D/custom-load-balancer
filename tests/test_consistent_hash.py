#!/usr/bin/env python3
"""
Unit tests for consistent hashing implementation.
Derrick Koros
"""

import unittest
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'load_balancer'))

from consistent_hash import ConsistentHash

class TestConsistentHash(unittest.TestCase):
    """Test cases for ConsistentHash class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.hash_ring = ConsistentHash(slots=512, virtual_servers=9)
    
    def test_initialization(self):
        """Test hash ring initialization."""
        self.assertEqual(self.hash_ring.slots, 512)
        self.assertEqual(self.hash_ring.virtual_servers, 9)
        self.assertEqual(len(self.hash_ring.ring), 512)
        self.assertEqual(len(self.hash_ring.servers), 0)
    
    def test_hash_functions(self):
        """Test hash function correctness."""
        # Test request hash function H(i) = i² + 2i + 17
        result = self.hash_ring.hash_request(100)
        expected = (100*100 + 2*100 + 17) % 512
        self.assertEqual(result, expected)
        
        # Test virtual server hash function Φ(i,j) = i² + j² + 2j + 25
        result = self.hash_ring.hash_virtual_server(5, 3)
        expected = (5*5 + 3*3 + 2*3 + 25) % 512
        self.assertEqual(result, expected)
    
    def test_add_server(self):
        """Test adding servers to the ring."""
        success = self.hash_ring.add_server(1, "server1")
        self.assertTrue(success)
        self.assertEqual(self.hash_ring.get_server_count(), 1)
        self.assertIn("server1", self.hash_ring.get_servers_list())
        
        # Test adding duplicate server
        success = self.hash_ring.add_server(1, "server1_duplicate")
        self.assertFalse(success)
        self.assertEqual(self.hash_ring.get_server_count(), 1)
    
    def test_remove_server(self):
        """Test removing servers from the ring."""
        # Add server first
        self.hash_ring.add_server(1, "server1")
        self.assertEqual(self.hash_ring.get_server_count(), 1)
        
        # Remove server
        success = self.hash_ring.remove_server(1)
        self.assertTrue(success)
        self.assertEqual(self.hash_ring.get_server_count(), 0)
        
        # Test removing non-existent server
        success = self.hash_ring.remove_server(999)
        self.assertFalse(success)
    
    def test_get_server(self):
        """Test request routing to servers."""
        # Add servers
        self.hash_ring.add_server(1, "server1")
        self.hash_ring.add_server(2, "server2")
        self.hash_ring.add_server(3, "server3")
        
        # Test request routing
        server = self.hash_ring.get_server(123456)
        self.assertIn(server, ["server1", "server2", "server3"])
        
        # Test with no servers
        empty_ring = ConsistentHash()
        server = empty_ring.get_server(123456)
        self.assertIsNone(server)
    
    def test_load_distribution(self):
        """Test load distribution across servers."""
        # Add servers
        servers = ["server1", "server2", "server3"]
        for i, server in enumerate(servers, 1):
            self.hash_ring.add_server(i, server)
        
        # Send many requests and check distribution
        request_counts = {server: 0 for server in servers}
        
        for request_id in range(1000, 11000):  # 10,000 requests
            server = self.hash_ring.get_server(request_id)
            if server:
                request_counts[server] += 1
        
        # Check that all servers received requests
        for server in servers:
            self.assertGreater(request_counts[server], 0)
        
        # Check load balance (no server should have more than 60% of requests)
        total_requests = sum(request_counts.values())
        for server in servers:
            load_percentage = request_counts[server] / total_requests
            self.assertLess(load_percentage, 0.6)
    
    def test_ring_integrity(self):
        """Test hash ring integrity validation."""
        # Add servers
        self.hash_ring.add_server(1, "server1")
        self.hash_ring.add_server(2, "server2")
        
        # Check integrity
        is_valid, issues = self.hash_ring.validate_ring_integrity()
        self.assertTrue(is_valid)
        self.assertEqual(len(issues), 0)

if __name__ == '__main__':
    unittest.main()