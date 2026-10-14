"""
IoT Simulator for MediPulse.

Acts like an ESP32 and sends fake vitals to the server, so the
Live Monitoring page can be demoed without real hardware.

Usage:
    python simulator.py                      # one device, ESP32-01
    python simulator.py ESP32-01 ESP32-02    # multiple devices
    python simulator.py --url http://192.168.1.5:8000 ESP32-01
"""
import random
import sys
import time

import requests

DEFAULT_URL = "http://127.0.0.1:8000"
INTERVAL = 2  # seconds between readings
API_KEY = "medipulse-demo-key"  # must match DEVICE_API_KEY in settings.py

def make_reading(device_id, critical):
    if critical:
        # abnormal values -> shows red alert on dashboard
        return {
            "device_id": device_id,
            "heart_rate": random.randint(122, 145),
            "spo2": random.randint(86, 91),
            "temperature": round(random.uniform(101.2, 103.5), 1),
            "bp_systolic": random.randint(150, 175),
            "bp_diastolic": random.randint(95, 110),
        }
    return {
        "device_id": device_id,
        "heart_rate": random.randint(65, 92),
        "spo2": random.randint(96, 99),
        "temperature": round(random.uniform(97.5, 98.9), 1),
        "bp_systolic": random.randint(110, 128),
        "bp_diastolic": random.randint(70, 85),
    }


def main():
    args = sys.argv[1:]
    url = DEFAULT_URL
    if "--url" in args:
        i = args.index("--url")
        url = args[i + 1].rstrip("/")
        del args[i:i + 2]
    devices = args or ["ESP32-01"]

    endpoint = f"{url}/api/vitals/"
    print(f"Sending to {endpoint} for devices: {', '.join(devices)}")
    print("Press Ctrl+C to stop. Every 10th reading is a critical one.\n")

    count = 0
    try:
        while True:
            count += 1
            critical = (count % 10 == 0)
            for device in devices:
                data = make_reading(device, critical)
                try:
                    r = requests.post(endpoint, json=data, headers={"X-API-Key": API_KEY}, timeout=5)
                    print(f"[{device}] HR {data['heart_rate']} | SpO2 {data['spo2']} | "
                          f"Temp {data['temperature']} -> {r.status_code} {r.text[:80]}")
                except requests.exceptions.RequestException as e:
                    print(f"[{device}] Could not reach server: {e}")
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nStopped.")


if __name__ == "__main__":
    main()