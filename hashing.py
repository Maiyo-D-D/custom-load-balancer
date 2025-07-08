import bisect
import hashlib

class ConsistentHash:
    def __init__(self, num_slots=512, vnodes=9):
        self.num_slots = num_slots
        self.vnodes = vnodes
        self.ring = []  # Sorted list of (position, server_name)
        self._occupied_slots = set() # Track occupied slots for collision handling

    def _server_id_to_int(self, server_name):
        # Convert server name to a consistent integer for hashing
        return int(hashlib.md5(str(server_name).encode()).hexdigest(), 16)

    def _hash_request(self, req_id):
        # Hash function for requests: H(i) = i + 2*i^2 + 17
        if not isinstance(req_id, int):
            raise TypeError("Request ID must be an integer.")
        return (req_id + 2 * req_id**2 + 17) % self.num_slots

    def _hash_server(self, server_int_id, vnode_j):
        # Hash function for servers: Φ(i,j) = i + j + 2*j^2 + 25
        return (server_int_id + vnode_j + 2 * vnode_j**2 + 25) % self.num_slots

    def add_server(self, server_name):
        server_int_id = self._server_id_to_int(server_name)
        for j in range(self.vnodes):
            pos = self._hash_server(server_int_id, j)
            
            # Linear probing to find next free slot on collision
            while pos in self._occupied_slots:
                pos = (pos + 1) % self.num_slots
            
            self._occupied_slots.add(pos)
            
            # Efficiently insert into sorted list
            bisect.insort(self.ring, (pos, server_name))

    def remove_server(self, server_name):
        # Rebuild the ring, excluding the removed server
        new_ring = []
        for pos, srv in self.ring:
            if srv == server_name:
                self._occupied_slots.remove(pos)
            else:
                new_ring.append((pos, srv))
        self.ring = new_ring

    def get_server(self, request_id):
        if not self.ring:
            return None
            
        pos = self._hash_request(request_id)
        
        # Get a list of positions for binary search
        positions = [item[0] for item in self.ring]
        
        # Find server using binary search (O(log M))
        index = bisect.bisect_left(positions, pos)
        
        # Handle wrap-around case
        if index == len(self.ring):
            index = 0
            
        return self.ring[index][1]