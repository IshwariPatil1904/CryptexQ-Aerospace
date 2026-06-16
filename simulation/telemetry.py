import random

def generate_telemetry():

    altitude = random.randint(30000, 40000)
    speed = random.randint(800, 900)

    message = f"""
Aircraft ID: AC102
Altitude: {altitude} ft
Speed: {speed} km/h
Engine Status: Normal
Navigation: Stable
"""

    return message