from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

app = Flask(__name__, static_folder='.')
CORS(app)

DATA_FILE = 'data.json'

# --- 1. CORE UTILITIES (Define these first) ---

def save_db(data):
    """Writes the dictionary to data.json with clean formatting."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_db():
    """Loads data.json. If it's missing, empty, or broken, resets it."""
    default_data = {
        "users": [
            {"user_id": "ADMIN01", "name": "System Admin", "role": "admin", "password": "password123"},
            {"user_id": "WAR01", "name": "Warden Sharma", "role": "warden", "password": "password123"},
            {"user_id": "STU001", "name": "Ayush Mahapatra", "role": "student", "password": "password123"}
        ],
        "students": [
            {"id": 1, "user_id": "STU001", "name": "Ayush Mahapatra", "roll": "2024H001", "room": "101", "status": "active", "contact": "9876543210"}
        ],
        "complaints": [],
        "visitors": []
    }

    if not os.path.exists(DATA_FILE):
        save_db(default_data)
        return default_data

    try:
        with open(DATA_FILE, 'r') as f:
            content = f.read().strip()
            if not content:
                save_db(default_data)
                return default_data
            return json.loads(content)
    except (json.JSONDecodeError, IOError):
        print("Data file corrupted. Resetting...")
        save_db(default_data)
        return default_data

# --- 2. API ENDPOINTS ---

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    db = load_db()
    # Find user matching ID, Password, and Role
    user = next((u for u in db['users'] if u['user_id'] == data.get('user_id') 
                 and u['password'] == data.get('password') 
                 and u['role'] == data.get('role')), None)
    
    if user:
        return jsonify({"success": True, "user": user})
    return jsonify({"success": False, "message": "Invalid Credentials"}), 401

@app.route('/api/students', methods=['GET'])
def get_students():
    return jsonify(load_db()['students'])

@app.route('/api/visitors', methods=['GET'])
def get_visitors():
    return jsonify(load_db().get('visitors', []))

@app.route('/api/complaints', methods=['GET'])
def get_complaints():
    return jsonify(load_db().get('complaints', []))

@app.route('/api/stats', methods=['GET'])
def get_stats():
    db = load_db()
    return jsonify({
        "total_students": len(db['students']),
        "active_students": len([s for s in db['students'] if s['status'] == 'active']),
        "open_complaints": len([c for c in db['complaints'] if c.get('status') == 'open'])
    })

# --- 3. SERVE FRONTEND ---

@app.route('/')
def index(): 
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def static_proxy(path): 
    return send_from_directory('.', path)

if __name__ == '__main__':
    print("HostelOS JSON Backend running on http://localhost:5000")
    app.run(debug=True, port=5000)
