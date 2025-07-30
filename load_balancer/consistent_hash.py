#!/usr/bin/env python3
"""
Distributed Systems Assignment 1 - Consistent Hashing Implementation
Task 2: Consistent hash map implementation

This module implements a consistent hashing algorithm using:
- 512 total slots in the hash ring
- 9 virtual servers per physical server (log₂(512))
- Hash function H(i) = i² + 2i + 17 for request mapping
- Hash function Φ(i,j) = i² + j² + 2j + 25 for virtual server mapping
- Linear probing for conflict resolution

The consistent hashing ensures:
1. Even load distribution across servers
2. Minimal redistribution when servers are added/removed
3. Clockwise request routing to nearest server

Author: Maiyo Dennis
"""

import logging
from typing import Optional, List, Dict, Tuple

logger = logging.getLogger(__name__)

class ConsistentHash:
    """
    Consistent Hash Ring implementation for load balancing.
    
    This class manages a circular hash ring with virtual servers
    to ensure even distribution of requests across server replicas.
    """
    
    def __init__(self, slots: int = 512, virtual_servers: int = 9):
        """
        Initialize the consistent hash ring.
        
        Args:
            slots: Total number of slots in the hash ring (default: 512)
            virtual_servers: Number of virtual servers per physical server (default: 9)
        """
        self.slots = slots
        self.virtual_servers = virtual_servers
        self.ring = [None] * slots  # Initialize empty ring
        self.servers = {}  # Server metadata storage
        
        logger.info(f"Initialized consistent hash with {slots} slots and {virtual_servers} virtual servers")
    
    def hash_request(self, request_id: int) -> int:
        """
        Hash function for mapping requests to ring positions.
        
        Uses the formula: H(i) = i² + 2i + 17
        
        Args:
            request_id: Unique identifier for the request
            
        Returns:
            Ring position (0 to slots-1)
        """
        hash_value = (request_id * request_id + 2 * request_id + 17) % self.slots
        logger.debug(f"Request {request_id} hashed to position {hash_value}")
        return hash_value
    
    def hash_virtual_server(self, server_id: int, virtual_id: int) -> int:
        """
        Hash function for mapping virtual servers to ring positions.
        
        Uses the formula: Φ(i,j) = i² + j² + 2j + 25
        
        Args:
            server_id: Physical server identifier
            virtual_id: Virtual server replica number (0 to virtual_servers-1)
            
        Returns:
            Ring position (0 to slots-1)
        """
        hash_value = (
            server_id * server_id + 
            virtual_id * virtual_id + 
            2 * virtual_id + 25
        ) % self.slots
        
        logger.debug(f"Virtual server ({server_id}, {virtual_id}) hashed to position {hash_value}")
        return hash_value
    
    def _find_next_available_slot(self, start_pos: int) -> Optional[int]:
        """
        Find the next available slot using linear probing.
        
        Args:
            start_pos: Starting position for search
            
        Returns:
            Next available slot position or None if ring is full
        """
        for i in range(self.slots):
            pos = (start_pos + i) % self.slots
            if self.ring[pos] is None:
                return pos
        return None  # Ring is full
    
    def add_server(self, server_id: int, hostname: str) -> bool:
        """
        Add a physical server with its virtual replicas to the ring.
        
        Args:
            server_id: Unique identifier for the server
            hostname: Server hostname/container name
            
        Returns:
            True if server was successfully added, False otherwise
        """
        if server_id in self.servers:
            logger.warning(f"Server {server_id} already exists")
            return False
        
        # Initialize server metadata
        self.servers[server_id] = {
            'hostname': hostname,
            'virtual_positions': []
        }
        
        # Add virtual servers to the ring
        for j in range(self.virtual_servers):
            initial_pos = self.hash_virtual_server(server_id, j)
            
            # Use linear probing to find available slot
            pos = self._find_next_available_slot(initial_pos)
            
            if pos is None:
                logger.error(f"Cannot add server {server_id}: ring is full")
                # Rollback: remove previously added virtual servers
                self._rollback_server_addition(server_id)
                return False
            
            # Place virtual server in the ring
            self.ring[pos] = server_id
            self.servers[server_id]['virtual_positions'].append(pos)
            
            logger.debug(f"Added virtual server ({server_id}, {j}) at position {pos}")
        
        logger.info(f"Successfully added server {server_id} ({hostname}) with {self.virtual_servers} virtual replicas")
        return True
    
    def _rollback_server_addition(self, server_id: int):
        """
        Remove partially added server in case of failure.
        
        Args:
            server_id: Server ID to rollback
        """
        if server_id in self.servers:
            # Remove virtual servers from ring
            for pos in self.servers[server_id]['virtual_positions']:
                self.ring[pos] = None
            
            # Remove server metadata
            del self.servers[server_id]
            logger.debug(f"Rolled back server {server_id}")
    
    def remove_server(self, server_id: int) -> bool:
        """
        Remove a server and all its virtual replicas from the ring.
        
        Args:
            server_id: Server identifier to remove
            
        Returns:
            True if server was successfully removed, False otherwise
        """
        if server_id not in self.servers:
            logger.warning(f"Server {server_id} not found for removal")
            return False
        
        hostname = self.servers[server_id]['hostname']
        
        # Remove all virtual servers from ring
        for pos in self.servers[server_id]['virtual_positions']:
            self.ring[pos] = None
            logger.debug(f"Removed virtual server at position {pos}")
        
        # Remove server metadata
        del self.servers[server_id]
        
        logger.info(f"Successfully removed server {server_id} ({hostname})")
        return True
    
    def get_server(self, request_id: int) -> Optional[str]:
        """
        Get the server hostname that should handle a given request.
        
        Uses clockwise traversal from the request's hash position
        to find the nearest server.
        
        Args:
            request_id: Request identifier
            
        Returns:
            Server hostname or None if no servers available
        """
        if not self.servers:
            logger.warning("No servers available to handle request")
            return None
        
        start_pos = self.hash_request(request_id)
        
        # Find next server in clockwise direction
        for i in range(self.slots):
            check_pos = (start_pos + i) % self.slots
            if self.ring[check_pos] is not None:
                server_id = self.ring[check_pos]
                hostname = self.servers[server_id]['hostname']
                
                logger.debug(f"Request {request_id} assigned to server {hostname} (ID: {server_id})")
                return hostname
        
        logger.error("Ring traversal completed but no server found")
        return None
    
    def get_servers_list(self) -> List[str]:
        """
        Get list of all active server hostnames.
        
        Returns:
            List of server hostnames
        """
        return [info['hostname'] for info in self.servers.values()]
    
    def get_server_count(self) -> int:
        """
        Get the number of active servers.
        
        Returns:
            Number of servers in the ring
        """
        return len(self.servers)
    
    def get_ring_status(self) -> Dict:
        """
        Get detailed status of the hash ring for debugging.
        
        Returns:
            Dictionary containing ring statistics
        """
        occupied_slots = sum(1 for slot in self.ring if slot is not None)
        
        return {
            'total_slots': self.slots,
            'occupied_slots': occupied_slots,
            'free_slots': self.slots - occupied_slots,
            'server_count': len(self.servers),
            'virtual_servers_per_physical': self.virtual_servers,
            'servers': {
                server_id: {
                    'hostname': info['hostname'],
                    'virtual_positions': info['virtual_positions']
                }
                for server_id, info in self.servers.items()
            }
        }
    
    def validate_ring_integrity(self) -> Tuple[bool, List[str]]:
        """
        Validate the integrity of the hash ring.
        
        Returns:
            Tuple of (is_valid, list_of_issues)
        """
        issues = []
        
        # Check for orphaned slots
        for pos, server_id in enumerate(self.ring):
            if server_id is not None and server_id not in self.servers:
                issues.append(f"Orphaned server {server_id} at position {pos}")
        
        # Check server virtual positions
        for server_id, info in self.servers.items():
            for pos in info['virtual_positions']:
                if pos >= self.slots or self.ring[pos] != server_id:
                    issues.append(f"Invalid virtual position {pos} for server {server_id}")
        
        is_valid = len(issues) == 0
        
        if is_valid:
            logger.info("Hash ring integrity check passed")
        else:
            logger.warning(f"Hash ring integrity issues found: {issues}")
        
        return is_valid, issues