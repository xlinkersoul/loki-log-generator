import requests
import random
import time
from datetime import datetime, timedelta, timezone

LOKI_URL = "https://loki.gogonggo.rke2.maas/loki/api/v1/push"
TENANT_ID = "otel"

TOTAL_LOGS = 5000
BATCH_SIZE = 1000


METHODS = ["GET", "POST"]
PATHS = ["/api/payment", "/api/auth", "/api/orders"]
USER_AGENTS = ["Mozilla/5.0", "curl/7.81.0", "PostmanRuntime/7.32.3"]

CLIENT_SUBNET = "192.168.1.0/25"
CLIENT_IPS = [
("172.16.1.1", 0.01),
("172.16.2.1", 0.01),
("172.16.3.1", 0.01),
("172.16.4.1", 0.01),
("172.16.5.1", 0.01),
("172.16.6.1", 0.01),
("172.16.7.1", 0.01),
("172.16.8.1", 0.01),
("172.16.9.1", 0.01),
("172.16.10.1", 0.01),
("172.16.11.1", 0.01),
("172.16.12.1", 0.01),
("172.16.13.1", 0.01),
("172.16.14.1", 0.01),
("172.16.15.1", 0.01),
("172.16.16.1", 0.01),
("172.16.17.1", 0.01),
("172.16.18.1", 0.01),
("172.16.19.1", 0.01),
("172.16.20.1", 0.01),
("172.16.21.1", 0.01),
("172.16.22.1", 0.01),
("172.16.23.1", 0.01),
("172.16.24.1", 0.01),
("172.16.25.1", 0.01),
("172.16.26.1", 0.01),
("172.16.27.1", 0.01),
("172.16.28.1", 0.01),
("172.16.29.1", 0.01),
("172.16.30.1", 0.01),
("172.16.31.1", 0.01),
("172.16.32.1", 0.01),
("172.16.33.1", 0.01),
("172.16.34.1", 0.01),
("172.16.35.1", 0.01),
("172.16.36.1", 0.01),
("172.16.37.1", 0.01),
("172.16.38.1", 0.01),
("172.16.39.1", 0.01),
("172.16.40.1", 0.01),
("172.16.41.1", 0.01),
("172.16.42.1", 0.01),
("172.16.43.1", 0.01),
("172.16.44.1", 0.01),
("172.16.45.1", 0.01),
("172.16.46.1", 0.01),
("172.16.47.1", 0.01),
("172.16.48.1", 0.01),
("172.16.49.1", 0.01),
("172.16.50.1", 0.01),
("172.16.51.1", 0.01),
("172.16.52.1", 0.01),
("172.16.53.1", 0.01),
("172.16.54.1", 0.01),
("172.16.55.1", 0.01),
("172.16.56.1", 0.01),
("172.16.57.1", 0.01),
("172.16.58.1", 0.01),
("172.16.59.1", 0.01),
("172.16.60.1", 0.01),
("172.16.61.1", 0.01),
("172.16.62.1", 0.01),
("172.16.63.1", 0.01),
("172.16.64.1", 0.01),
("172.16.65.1", 0.01),
("172.16.66.1", 0.01),
("172.16.67.1", 0.01),
("172.16.68.1", 0.01),
("172.16.69.1", 0.01),
("172.16.70.1", 0.01),
("172.16.71.1", 0.01),
("172.16.72.1", 0.01),
("172.16.73.1", 0.01),
("172.16.74.1", 0.01),
("172.16.75.1", 0.01),
("172.16.76.1", 0.01),
("172.16.77.1", 0.01),
("172.16.78.1", 0.01),
("172.16.79.1", 0.01),
("172.16.80.1", 0.01),
("172.16.81.1", 0.01),
("172.16.82.1", 0.01),
("172.16.83.1", 0.01),
("172.16.84.1", 0.01),
("172.16.85.1", 0.01),
("172.16.86.1", 0.01),
("172.16.87.1", 0.01),
("172.16.88.1", 0.01),
("172.16.89.1", 0.01),
("172.16.90.1", 0.01),
("172.16.91.1", 0.01),
("172.16.92.1", 0.01),
("172.16.93.1", 0.01),
("172.16.94.1", 0.01),
("172.16.95.1", 0.01),
("172.16.96.1", 0.01),
("172.16.97.1", 0.01),
("172.16.98.1", 0.01),
("172.16.99.1", 0.01),
("172.16.100.1", 0.01)
]

def choose_client_ip():
    r = random.random()
    cumulative = 0
    for ip, prob in CLIENT_IPS:
        cumulative += prob
        if r <= cumulative:
            return ip
    # If none selected, generate random IP from subnet
    # Parse the subnet to get network and mask
    import ipaddress
    net = ipaddress.IPv4Network(CLIENT_SUBNET, strict=False)
    # Get a random host in the subnet
    host = random.randint(0, (1 << (32 - net.prefixlen))) 
    ip_bytes = net.network_address + host
    return str(ip_bytes)


def generate_access_log(i):
    now = datetime.now(timezone.utc)
    ts_ns = str(int(now.timestamp() * 1e9))

    ip = choose_client_ip()
    method = random.choice(METHODS)
    path = random.choice(PATHS)
    status = random.choice([200, 200, 200, 200, 500])  # mostly 200
    size = random.randint(200, 1500)
    ua = random.choice(USER_AGENTS)

    # NGINX-style access log format
    # log_line = "hello-world"
    log_line = (
        f'V5 - {ip} - - [{now.strftime("%d/%b/%Y:%H:%M:%S +0000")}] '
        f'"{method} {path} HTTP/1.1" {status} {size} "-" "{ua}"'
    )

    stream = {
        "stream": {
            "job": "poc",
            "app": "gateway",
        },
        "values": [[ts_ns, log_line]]
    }

    return stream


def push_logs():
    streams = []
    for i in range(TOTAL_LOGS):
        streams.append(generate_access_log(i))

    for i in range(0, len(streams), BATCH_SIZE):
        payload = {"streams": streams[i:i+BATCH_SIZE]}
        headers = {
            "Content-Type": "application/json",
            "X-Scope-OrgID": TENANT_ID
        }
        r = requests.post(
            LOKI_URL,
            json=payload,
            headers=headers,
            verify=False
        )
        print(f"Batch {i//BATCH_SIZE + 1} -> {r.status_code}")
        # Print debug information
        print(f"URL: {r.request.url}")
        print(f"Headers: {r.request.headers}")
        print(f"Body: {r.request.body.decode()}")
        # if r.status_code != 200:
        #     print(f"Debug response: {r.text}")
        time.sleep(0.1)


if __name__ == "__main__":
    push_logs()

