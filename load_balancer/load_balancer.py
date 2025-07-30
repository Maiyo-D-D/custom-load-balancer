from flask import Flask, request, jsonify
from consistent_hash import ConsistentHash
import requests
import threading

app = Flask(__name__)
hash_ring = ConsistentHash(slots=512, virtual_servers=9)
server_id_counter = 1
lock = threading.Lock()

@app.route('/add', methods=['POST'])
def add_server():
    data = request.get_json()
    n = data.get('n', 1)
    hostnames = data.get('hostnames', [])
    added = []
    global server_id_counter
    with lock:
        for i in range(n):
            hostname = hostnames[i] if i < len(hostnames) else f"Server{server_id_counter}"
            success = hash_ring.add_server(server_id_counter, hostname)
            if success:
                added.append(hostname)
                server_id_counter += 1
    return jsonify({"message": {"added": added, "N": hash_ring.get_server_count()}}), 200

@app.route('/rm', methods=['DELETE'])
def remove_server():
    data = request.get_json()
    n = data.get('n', 1)
    removed = []
    with lock:
        ids = list(hash_ring.servers.keys())[:n]
        for sid in ids:
            hostname = hash_ring.servers[sid]['hostname']
            success = hash_ring.remove_server(sid)
            if success:
                removed.append(hostname)
    return jsonify({"message": {"removed": removed, "N": hash_ring.get_server_count()}}), 200

@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({"message": {
        "N": hash_ring.get_server_count(),
        "replicas": hash_ring.get_servers_list()
    }}), 200

@app.route('/home', methods=['GET'])
def home():
    request_id = request.args.get('id', default=1, type=int)
    server = hash_ring.get_server(request_id)
    if server is None:
        return jsonify({"message": "No servers available", "status": "failure"}), 503
    try:
        # Use localhost for demo, or actual hostname if in Docker network
        resp = requests.get(f"http://{server}:5000/home", timeout=2)
        return jsonify(resp.json()), resp.status_code
    except Exception:
        return jsonify({"message": f"Server {server} unreachable", "status": "failure"}), 502

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"message": "Endpoint not found", "status": "failure"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True)