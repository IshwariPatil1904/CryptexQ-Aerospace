from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO

from core.hybrid_crypto import generate_hybrid_key

from nodes.aircraft import aircraft_send
from nodes.satellite import relay_packet
from nodes.ground import ground_receive

from core.encryption import decrypt_message

from ai.anomaly_detector import detect_anomaly

app = Flask(__name__)

socketio = SocketIO(
    app,
    async_mode="eventlet",
    cors_allowed_origins="*"
)

# Store latest encrypted packet
latest_packet = {}


# ---------------- DASHBOARD ---------------- #

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/network")
def network():

    return render_template("network.html")


@app.route("/security")
def security():

    return render_template("security.html")


@app.route("/about")
def about():

    return render_template("about.html")

# ---------------- ATTACKER PAGE ---------------- #

@app.route("/attacker")
def attacker():
    return render_template("attacker.html")


# ---------------- START SECURE TRANSMISSION ---------------- #

@app.route("/start")
def start_secure_transmission():

    global latest_packet

    # Generate hybrid session key
    key = generate_hybrid_key()

    # Aircraft encrypts telemetry
    (
        telemetry,
        nonce,
        encrypted,
        signature,
        public_key

    ) = aircraft_send(key)

    # ---------------- AI ANOMALY DETECTION ---------------- #

    try:

        lines = telemetry.splitlines()

        altitude = int(
            lines[2]
            .split(":")[1]
            .replace("ft", "")
            .strip()
        )

        speed = int(
            lines[3]
            .split(":")[1]
            .replace("km/h", "")
            .strip()
        )

        result = detect_anomaly(
            altitude,
            speed
        )

        if result == -1:

            print("[AI ENGINE]")
            print("Anomalous telemetry detected")

            socketio.emit(

                "attack_detected",

                {   "type": "AI",
                    "msg":
                    "AI anomaly detection triggered"
                }
            )

    except Exception as e:

        print("[AI ERROR]")
        print(e)

    # ------------------------------------------------------ #

    # Satellite relays encrypted packet
    nonce, encrypted = relay_packet(
        nonce,
        encrypted
    )

    # Ground station decrypts packet
    decrypted = ground_receive(

        key,

        nonce,

        encrypted,

        signature,

        public_key
    )

    # Store packet for attack simulation
    latest_packet = {

        "key": key,
        "nonce": nonce,
        "encrypted": encrypted
    }

    return jsonify({

        "status":
            "Secure transmission complete",

        "encrypted":
            encrypted.hex(),

        "decrypted":
            decrypted
    })


# ---------------- MITM ATTACK ---------------- #

@socketio.on("launch_attack")
def attack():

    global latest_packet

    # Prevent attack before transmission exists
    if not latest_packet:

        socketio.emit(
            "attack_detected",
            {
                "msg":
                "No active secure transmission"
            }
        )

        return

    try:

        # Copy encrypted packet
        tampered = bytearray(
            latest_packet["encrypted"]
        )

        # Modify ciphertext
        tampered[5] ^= 0xFF

        print("\n[ATTACKER]")
        print("Ciphertext modified")

        # Attempt decryption
        decrypt_message(

            latest_packet["key"],

            latest_packet["nonce"],

            bytes(tampered)
        )

    except Exception:

        print("[CryptexQ]")
        print("MITM attack detected")
        print("AES-GCM integrity verification failed\n")

        socketio.emit(

            "attack_detected",

            {   "type": "MITM",
                "msg":
                "AES-GCM integrity verification failed"
            }
        )

@socketio.on("spoof_attack")
def spoof_attack():

    print("\n[ATTACKER]")
    print("Telemetry spoofing injected")

    # Fake abnormal telemetry
    fake_telemetry = {

        "altitude": 120000,

        "speed": 3500,

        "status": "SPOOFED"
    }

    # Run AI detection
    result = detect_anomaly(

        fake_telemetry["altitude"],

        fake_telemetry["speed"]
    )

    # If anomaly detected
    if result == -1:

        print("[AI ENGINE]")
        print("Spoofed telemetry detected")

        # Send alert
        socketio.emit(

            "attack_detected",

            {

                "type": "AI",

                "msg":
                "Telemetry spoofing detected"
            }
        )

        # Send fake telemetry to dashboard
        socketio.emit(

            "telemetry_spoofed",

            fake_telemetry
        )
# ---------------- MAIN ---------------- #

if __name__ == "__main__":

    socketio.run(
        app,
        host="127.0.0.1",
        port=5050,
        debug=True
    )