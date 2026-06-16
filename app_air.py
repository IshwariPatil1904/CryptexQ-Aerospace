import requests
import time
import random
import json
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Ground station configuration
SERVER_URL = "http://127.0.0.1:5050/api/telemetry"
SHARED_SECRET = b"AviationSecretKey123!" 
AES_KEY = hashlib.sha256(SHARED_SECRET).digest()[:16]

# Flags configured dynamically or manually
ENCRYPTION_ON = True 

def generate_telemetry():
    return {
        "aircraft": "AC102",
        "altitude": random.randint(35000, 37000),
        "speed": random.randint(820, 860),
        "fuel": max(0, random.randint(70, 90)),
        "engine": "Normal",
        "navigation": "Operational"
    }

def encrypt_data(plaintext_str):
    """Encrypt using standard AES-CBC 128-bit"""
    iv = os.urandom(16)
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    padded_data = pad(plaintext_str.encode('utf-8'), AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    
    # Return Base64 strings clean for JSON transfer
    return {
        "payload": base64.b64encode(encrypted).decode('utf-8'),
        "iv": base64.b64encode(iv).decode('utf-8')
    }

if __name__ == "__main__":
    import os
    print("🛫 Launching Aircraft Flight Computer System...")
    
    while True:
        telemetry = generate_telemetry()
        raw_json_str = json.dumps(telemetry)
        
        if ENCRYPTION_ON:
            crypto_package = encrypt_data(raw_json_str)
            packet = {
                "encrypted": True,
                "payload": crypto_package["payload"],
                "iv": crypto_package["iv"]
            }
        else:
            packet = {
                "encrypted": False,
                "payload": raw_json_str,
                "iv": ""
            }
            
        try:
            # Broadcast over the wire to the server
            response = requests.post(SERVER_URL, json=packet)
        except requests.exceptions.ConnectionError:
            print("❌ Connection down. Scanning for ground control towers...")
            
        time.sleep(1) # Send transmission every 1 second