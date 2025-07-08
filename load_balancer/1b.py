from flask import Flask, request, jsonify
from hashing import ConsistentHash
import os, subprocess

app = Flask(__name__)
servers = ["Server1", "Server2", "Server3"]
hash_map = ConsistentHash(servers)
server_count = 3

@app.route('/rep', methods=['GET'])
def rep():
    return jsonify({"message": {"N": len(servers), "replicas": servers}, "status": "successful"}), 200

@app.route('/add', methods=['POST'])
def add():
    global server_count
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])
    if len(hostnames) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than newly added instances", "status": "failure"}), 400

    for i in range(n):
        name = hostnames[i] if i < len(hostnames) else f"S{server_count + i + 1}"
        subprocess.run(["docker", "run", "-d", "--network", "net1", "--name", name, "-e", f"SERVER_ID={name}", "custom-server"])
        hash_map.add_server(name)
        servers.append(name)
    server_count += n
    return jsonify({"message": {"N": len(servers), "replicas": servers}, "status": "successful"}), 200

@app.route('/rm', methods=['DELETE'])
def remove():
    data = request.get_json()
    n = data.get("n")
    hostnames = data.get("hostnames", [])
    if len(hostnames) > n:
        return jsonify({"message": "<Error> Length of hostname list is more than removable instances", "status": "failure"}), 400
    removed = []
    for name in hostnames:
        subprocess.run(["docker", "rm", "-f", name])
        hash_map.remove_server(name)
        servers.remove(name)
        removed.append(name)
    return jsonify({"message": {"N": len(servers), "replicas": servers}, "status": "successful"}), 200

@app.route('/<path:endpoint>', methods=['GET'])
def route_request(endpoint):
    key = request.remote_addr
    target = hash_map.get_server(key)
    try:
        import requests
        res = requests.get(f"http://{target}:5000/{endpoint}")
        return res.content, res.status_code
    except:
        return jsonify({"message": f"Server {target} unreachable", "status": "failure"}), 503

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
