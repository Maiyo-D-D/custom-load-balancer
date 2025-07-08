import hashlib
import bisect

class ConsistentHash:
    def __init__(self, servers=None, num_slots=512, vnodes=9):
        self.num_slots = num_slots
        self.vnodes = vnodes
        self.ring = []
        self.server_map = {}
        if servers:
            for s in servers:
                self.add_server(s)

    def _hash(self, key):
        return int(hashlib.sha1(str(key).encode()).hexdigest(), 16) % self.num_slots

    def add_server(self, server):
        for j in range(self.vnodes):
            vnode_key = f"{server}-{j}"
            pos = self._hash(vnode_key)
            self.ring.append((pos, server))
        self.ring.sort()

    def remove_server(self, server):
        self.ring = [(pos, srv) for pos, srv in self.ring if srv != server]

    def get_server(self, key):
        pos = self._hash(key)
        for ring_pos, srv in self.ring:
            if ring_pos >= pos:
                return srv
        return self.ring[0][1]