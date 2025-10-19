import os
import datetime
from functools import wraps
import logging

import jwt
from dotenv import load_dotenv
from flask import Flask, jsonify, request, g
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()
app = Flask(__name__)
app.config["JWT_SECRET"] = os.getenv("JWT_SECRET")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

hashed_password = generate_password_hash("password123", method="pbkdf2:sha256")

users = {
    "user1@example.com": {
        "id": 1,
        "email": "user1@example.com",
        "password_hash": hashed_password,
        "name": "Bisma Gang",
    }
}

items = [
    {"id": 1, "name": "Laptop Lenovo Legion", "price": 25000000},
    {"id": 2, "name": "Mechanical Keyboard Logitech", "price": 1500000},
    {"id": 3, "name": "Wireless Mouse Ignix F1", "price": 750000},
]


def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            parts = request.headers["Authorization"].split()
            if len(parts) == 2 and parts[0].lower() == "bearer":
                token = parts[1]

        if not token:
            return jsonify({"error": "Missing or invalid Authorization header"}), 401

        try:
            payload = jwt.decode(token, app.config["JWT_SECRET"], algorithms=["HS256"])
            g.user = users.get(payload["sub"])
            if not g.user:
                return jsonify({"error": "User not found"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
            
        return f(*args, **kwargs)

    return decorated

@app.route("/auth/login", methods=["POST"])
def login():
    """Endpoint untuk autentikasi user dan memberikan JWT."""
    data = request.get_json()
    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"error": "Email and password are required"}), 400

    email = data["email"]
    password = data["password"]

    user = users.get(email)

    if not user or not check_password_hash(user["password_hash"], password):
        logging.warning(f"Login failed for email: {email}")
        return jsonify({"error": "Invalid credentials"}), 401

    payload = {
        "sub": user["email"],  
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15), 
        "iat": datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, app.config["JWT_SECRET"], algorithm="HS256")
    logging.info(f"Login successful for email: {email}")
    
    return jsonify({"access_token": token})


@app.route("/items", methods=["GET"])
def get_items():
    """Endpoint publik untuk melihat semua item."""
    return jsonify({"items": items})


@app.route("/profile", methods=["PUT"])
@jwt_required
def update_profile():
    """Endpoint terproteksi untuk mengubah nama atau email user."""
    data = request.get_json()
    if not data or ("name" not in data and "email" not in data):
        return jsonify({"error": "At least one field (name or email) is required"}), 400

    current_user = g.user
    
    if "name" in data and isinstance(data["name"], str) and data["name"].strip():
        current_user["name"] = data["name"].strip()

    if "email" in data and isinstance(data["email"], str) and data["email"].strip():
       current_user["email"] = data["email"].strip()

    logging.info(f"Profile updated for user: {current_user['email']}")
    return jsonify({
        "message": "Profile updated",
        "profile": {"name": current_user["name"], "email": current_user["email"]}
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)