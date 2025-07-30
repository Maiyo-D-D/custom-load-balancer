#!/usr/bin/env python3
"""
Distributed Systems Assignment 1 - Performance Analysis and Testing
Task 4: Analysis and testing of load balancer performance

This module provides comprehensive testing including:
1. Load distribution analysis (A-1)
2. Scalability analysis (A-2)
3. Endpoint functionality testing (A-3)
4. Hash function modification testing (A-4)

Author: Edwin Kuria
"""

import asyncio
import aiohttp
import requests
import matplotlib.pyplot as plt
import numpy as np
import json
import time
import logging
from collections import defaultdict, Counter
from typing import Dict, List, Tuple
import os
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('analysis/logs/performance_analysis.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configuration
BASE_URL = "http://localhost:5000"
ANALYSIS_DIR = "analysis"
CHARTS_DIR = f"{ANALYSIS_DIR}/charts"
LOGS_DIR = f"{ANALYSIS_DIR}/logs"

# Ensure directories exist
os.makedirs(CHARTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)

class LoadBalancerTester:
    """Comprehensive testing suite for the load balancer."""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    async def send_request(self, endpoint: str) -> Dict:
        """
        Send an async HTTP request to the load balancer.
        
        Args:
            endpoint: The endpoint to request
            
        Returns:
            Response data or None if request failed
        """
        try:
            async with self.session.get(f"{self.base_url}/{endpoint}") as response:
                return {
                    'data': await response.json(),
                    'status_code': response.status,
                    'success': True
                }
        except Exception as e:
            logger.error(f"Request to {endpoint} failed: {str(e)}")
            return {'success': False, 'error': str(e)}
    
    def set_server_count(self, target_count: int) -> bool:
        """
        Adjust the number of servers to target count.
        
        Args:
            target_count: Desired number of servers
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current server count
            response = requests.get(f"{self.base_url}/rep", timeout=10)
            current_count = response.json()["message"]["N"]
            
            if target_count > current_count:
                # Add servers
                diff = target_count - current_count
                response = requests.post(
                    f"{self.base_url}/add",
                    json={"n": diff},
                    timeout=30
                )
                return response.status_code == 200
                
            elif target_count < current_count:
                # Remove servers
                diff = current_count - target_count
                response = requests.delete(
                    f"{self.base_url}/rm",
                    json={"n": diff},
                    timeout=30
                )
                return response.status_code == 200
            
            return True  # Already at target count
            
        except Exception as e:
            logger.error(f"Failed to set server count to {target_count}: {str(e)}")
            return False
    
    async def run_load_test(self, num_requests: int, num_servers: int = 3) -> Dict[str, int]:
        """
        Run a load test with specified parameters.
        
        Args:
            num_requests: Number of requests to send
            num_servers: Number of servers to test with
            
        Returns:
            Dictionary mapping server IDs to request counts
        """
        logger.info(f"Starting load test: {num_requests} requests, {num_servers} servers")
        
        # Set up servers
        if not self.set_server_count(num_servers):
            logger.error("Failed to set up servers for load test")
            return {}
        
        # Wait for configuration to stabilize
        time.sleep(3)
        
        # Send requests concurrently
        server_counts = defaultdict(int)
        successful_requests = 0
        failed_requests = 0
        
        tasks = []
        for i in range(num_requests):
            task = self.send_request("home")
            tasks.append(task)
        
        # Execute all requests
        results = await asyncio.gather(*tasks)
        
        # Process results
        for result in results:
            if result['success'] and result['status_code'] == 200:
                try:
                    message = result['data']['message']
                    # Extract server ID from message "Hello from Server: X"
                    server_id = message.split("Server: ")[1]
                    server_counts[server_id] += 1
                    successful_requests += 1
                except (KeyError, IndexError) as e:
                    logger.warning(f"Failed to parse server ID from response: {e}")
                    failed_requests += 1
            else:
                failed_requests += 1
        
        logger.info(f"Load test completed: {successful_requests} successful, {failed_requests} failed")
        return dict(server_counts)
    
    def test_all_endpoints(self) -> Dict[str, bool]:
        """
        Test all load balancer endpoints.
        
        Returns:
            Dictionary mapping endpoint names to success status
        """
        results = {}
        
        logger.info("Testing all endpoints...")
        
        # Test /rep endpoint
        try:
            response = requests.get(f"{self.base_url}/rep", timeout=10)
            results['/rep'] = response.status_code == 200
            logger.info(f"/rep endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            results['/rep'] = False
            logger.error(f"/rep endpoint failed: {e}")
        
        # Test /add endpoint
        try:
            response = requests.post(
                f"{self.base_url}/add",
                json={"n": 1, "hostnames": ["TestServer1"]},
                timeout=30
            )
            results['/add'] = response.status_code == 200
            logger.info(f"/add endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            results['/add'] = False
            logger.error(f"/add endpoint failed: {e}")
        
        # Test /rm endpoint
        try:
            response = requests.delete(
                f"{self.base_url}/rm",
                json={"n": 1},
                timeout=30
            )
            results['/rm'] = response.status_code == 200
            logger.info(f"/rm endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            results['/rm'] = False
            logger.error(f"/rm endpoint failed: {e}")
        
        # Test /home endpoint
        try:
            response = requests.get(f"{self.base_url}/home", timeout=10)
            results['/home'] = response.status_code == 200
            logger.info(f"/home endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            results['/home'] = False
            logger.error(f"/home endpoint failed: {e}")
        
        # Test invalid endpoint
        try:
            response = requests.get(f"{self.base_url}/invalid", timeout=10)
            results['/invalid'] = response.status_code == 400
            logger.info(f"/invalid endpoint: {response.status_code} - {response.json()}")
        except Exception as e:
            results['/invalid'] = False
            logger.error(f"/invalid endpoint test failed: {e}")
        
        return results

class PerformanceAnalyzer:
    """Handles performance analysis and visualization."""
    
    @staticmethod
    def analyze_load_distribution(server_counts: Dict[str, int], title: str = "Load Distribution") -> None:
        """
        Create bar chart for load distribution analysis.
        
        Args:
            server_counts: Dictionary mapping server IDs to request counts
            title: Chart title
        """
        if not server_counts:
            logger.warning("No data to analyze for load distribution")
            return
        
        servers = list(server_counts.keys())
        counts = list(server_counts.values())
        
        plt.figure(figsize=(12, 8))
        bars = plt.bar(servers, counts, color='skyblue', edgecolor='navy', alpha=0.7)
        
        # Add value labels on bars
        for bar, count in zip(bars, counts):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(counts)*0.01,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        plt.title(f'{title}\nTotal Requests: {sum(counts)}', fontsize=16, fontweight='bold')
        plt.xlabel('Server ID', fontsize=12)
        plt.ylabel('Request Count', fontsize=12)
        plt.xticks(rotation=45)
        plt.grid(axis='y', alpha=0.3)
        
        # Add statistics
        mean_load = np.mean(counts)
        std_load = np.std(counts)
        plt.axhline(y=mean_load, color='red', linestyle='--', alpha=0.7, 
                   label=f'Mean: {mean_load:.1f}')
        plt.legend()
        
        plt.tight_layout()
        filename = f"{CHARTS_DIR}/load_distribution_{int(time.time())}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        logger.info(f"Load distribution chart saved to {filename}")
        plt.show()
        
        # Log statistics
        logger.info(f"Load Distribution Statistics:")
        logger.info(f"  Mean load per server: {mean_load:.2f}")
        logger.info(f"  Standard deviation: {std_load:.2f}")
        logger.info(f"  Min load: {min(counts)}")
        logger.info(f"  Max load: {max(counts)}")
        logger.info(f"  Load variance: {std_load**2:.2f}")
    
    @staticmethod
    def analyze_scalability(scalability_data: Dict[int, float]) -> None:
        """
        Create line chart for scalability analysis.
        
        Args:
            scalability_data: Dictionary mapping server counts to average loads
        """
        if not scalability_data:
            logger.warning("No data to analyze for scalability")
            return
        
        server_counts = list(scalability_data.keys())
        average_loads = list(scalability_data.values())
        
        plt.figure(figsize=(12, 8))
        plt.plot(server_counts, average_loads, marker='o', linewidth=2, 
                markersize=8, color='darkblue', markerfacecolor='lightblue', 
                markeredgecolor='darkblue', markeredgewidth=2)
        
        # Add value labels
        for x, y in zip(server_counts, average_loads):
            plt.annotate(f'{y:.1f}', (x, y), textcoords="offset points", 
                        xytext=(0,10), ha='center', fontweight='bold')
        
        plt.title('Scalability Analysis: Average Load per Server vs Number of Servers', 
                 fontsize=16, fontweight='bold')
        plt.xlabel('Number of Servers', fontsize=12)
        plt.ylabel('Average Load per Server', fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.xticks(server_counts)
        
        # Add trend line
        z = np.polyfit(server_counts, average_loads, 1)
        p = np.poly1d(z)
        plt.plot(server_counts, p(server_counts), "--", alpha=0.7, color='red',
                label=f'Trend: {z[0]:.1f}x + {z[1]:.1f}')
        plt.legend()
        
        plt.tight_layout()
        filename = f"{CHARTS_DIR}/scalability_analysis_{int(time.time())}.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        logger.info(f"Scalability chart saved to {filename}")
        plt.show()
        
        # Log analysis
        logger.info(f"Scalability Analysis:")
        for servers, avg_load in scalability_data.items():
            logger.info(f"  {servers} servers: {avg_load:.2f} avg load")

async def run_analysis_a1():
    """Analysis A-1: Load distribution with 10,000 requests on 3 servers."""
    logger.info("=== Starting Analysis A-1: Load Distribution ===")
    
    async with LoadBalancerTester() as tester:
        result = await tester.run_load_test(10000, 3)
        
        if result:
            PerformanceAnalyzer.analyze_load_distribution(
                result, 
                "A-1: Load Distribution Analysis (10,000 requests, 3 servers)"
            )
            
            # Calculate and log load balancing efficiency
            total_requests = sum(result.values())
            expected_load = total_requests / len(result)
            actual_loads = list(result.values())
            variance = np.var(actual_loads)
            
            logger.info(f"Load Balancing Efficiency:")
            logger.info(f"  Expected load per server: {expected_load:.2f}")
            logger.info(f"  Actual load variance: {variance:.2f}")
            logger.info(f"  Load balancing quality: {'Good' if variance < expected_load * 0.1 else 'Needs improvement'}")
        else:
            logger.error("A-1 analysis failed - no data collected")

async def run_analysis_a2():
    """Analysis A-2: Scalability test with 2-6 servers."""
    logger.info("=== Starting Analysis A-2: Scalability Analysis ===")
    
    scalability_results = {}
    
    async with LoadBalancerTester() as tester:
        for num_servers in range(2, 7):
            logger.info(f"Testing scalability with {num_servers} servers...")
            
            result = await tester.run_load_test(10000, num_servers)
            
            if result:
                avg_load = sum(result.values()) / len(result)
                scalability_results[num_servers] = avg_load
                logger.info(f"Average load with {num_servers} servers: {avg_load:.2f}")
            else:
                logger.error(f"Failed to collect data for {num_servers} servers")
    
    if scalability_results:
        PerformanceAnalyzer.analyze_scalability(scalability_results)
    else:
        logger.error("A-2 analysis failed - no scalability data collected")

def run_analysis_a3():
    """Analysis A-3: Endpoint testing and failure recovery."""
    logger.info("=== Starting Analysis A-3: Endpoint Testing and Failure Recovery ===")
    
    tester = LoadBalancerTester()
    
    # Test all endpoints
    endpoint_results = tester.test_all_endpoints()
    
    logger.info("Endpoint Test Results:")
    for endpoint, success in endpoint_results.items():
        status = "PASS" if success else "FAIL"
        logger.info(f"  {endpoint}: {status}")
    
    # Test failure recovery
    logger.info("Testing failure recovery...")
    
    try:
        # Get initial server list
        response = requests.get(f"{BASE_URL}/rep", timeout=10)
        initial_servers = response.json()["message"]["replicas"]
        logger.info(f"Initial servers: {initial_servers}")
        
        # Simulate server failure by stopping a container
        if initial_servers:
            server_to_stop = initial_servers[0]
            logger.info(f"Simulating failure of server: {server_to_stop}")
            
            # Stop the server container
            os.system(f'sudo docker stop {server_to_stop} 2>/dev/null')
            
            # Wait for health check to detect failure and recover
            logger.info("Waiting for failure detection and recovery...")
            time.sleep(15)
            
            # Check if a new server was spawned
            response = requests.get(f"{BASE_URL}/rep", timeout=10)
            new_servers = response.json()["message"]["replicas"]
            logger.info(f"Servers after recovery: {new_servers}")
            
            if len(new_servers) == len(initial_servers):
                logger.info("SUCCESS: Load balancer maintained server count after failure")
            else:
                logger.warning("WARNING: Server count changed after failure")
        
    except Exception as e:
        logger.error(f"Failure recovery test failed: {e}")

async def run_analysis_a4():
    """Analysis A-4: Modified hash functions testing."""
    logger.info("=== Starting Analysis A-4: Modified Hash Functions ===")
    
    # This would require modifying the hash functions in consistent_hash.py
    # For demonstration, we'll test the current implementation and suggest modifications
    
    logger.info("Current hash functions:")
    logger.info("  H(i) = i² + 2i + 17 (request mapping)")
    logger.info("  Φ(i,j) = i² + j² + 2j + 25 (virtual server mapping)")
    
    async with LoadBalancerTester() as tester:
        # Test with current hash functions
        original_result = await tester.run_load_test(10000, 3)
        
        if original_result:
            logger.info("Results with original hash functions:")
            for server, count in original_result.items():
                logger.info(f"  Server {server}: {count} requests")
            
            PerformanceAnalyzer.analyze_load_distribution(
                original_result,
                "A-4: Load Distribution with Original Hash Functions"
            )
    
    # Suggestions for modified hash functions
    logger.info("\nSuggested alternative hash functions for testing:")
    logger.info("1. H(i) = (i * 2654435761) % 2^32  # Knuth's multiplicative hash")
    logger.info("2. Φ(i,j) = ((i << 16) + j) * 2654435761 % 2^32")
    logger.info("3. H(i) = i * i * i + 7  # Cubic function")
    logger.info("4. Φ(i,j) = (i + j) * (i + j + 1) / 2 + j  # Cantor pairing")

async def main():
    """Main analysis runner."""
    logger.info("Starting comprehensive load balancer analysis...")
    
    # Check if load balancer is running
    try:
        response = requests.get(f"{BASE_URL}/rep", timeout=5)
        if response.status_code != 200:
            logger.error("Load balancer is not responding properly")
            return
    except Exception as e:
        logger.error(f"Cannot connect to load balancer at {BASE_URL}: {e}")
        logger.error("Please ensure the load balancer is running with 'make run'")
        return
    
    # Run all analyses
    try:
        await run_analysis_a1()
        await run_analysis_a2()
        run_analysis_a3()
        await run_analysis_a4()
        
        logger.info("All analyses completed successfully!")
        
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        raise

if __name__ == "__main__":
    # Install required packages if not present
    try:
        import matplotlib.pyplot as plt
        import aiohttp
    except ImportError:
        logger.error("Required packages not installed. Run: pip install matplotlib aiohttp")
        sys.exit(1)
    
    # Run the analysis
    asyncio.run(main())