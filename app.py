from flask import Flask, render_template, jsonify
import random
import hashlib
import time

app = Flask(__name__)

def generate_telemetry():
    return {
        "aircraft": "AC102",
        "altitude": random.randint(35000, 39000),
        "speed": random.randint(800, 900),
        "fuel": random.randint(60, 100),
        "engine": "Normal",
        "navigation": "Stable"
    }

def encrypt_packet(data):

    payload = str(data)

    encrypted = hashlib.sha256(payload.encode()).hexdigest()

    return encrypted

@app.route("/")
def home():
    return render_template("dashboard.html")


@app.route("/start")
def start():

    telemetry = generate_telemetry()

    encrypted = encrypt_packet(telemetry)

    response = {
        "status": "Secure transmission complete",
        "encrypted": encrypted,
        "decrypted": telemetry
    }

    return jsonify(response)


@app.route("/attack")
def attack():

    response = {
        "status": "⚠ MITM Attack Detected — Transmission Blocked"
    }

    return jsonify(response)


if __name__ == "__main__":
    app.run(debug=True)