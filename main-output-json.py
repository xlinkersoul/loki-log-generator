import requests
import random
import time
import json
from datetime import datetime, timezone
import ipaddress

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
    # ... (keep the rest same)
    ("172.16.100.1", 0.01)
]


def choose_client_ip():
    r = random.random()
    cumulative = 0
    for ip, prob in CLIENT_IPS:
        cumulative += prob
        if r <= cumulative:
            return ip

    net = ipaddress.IPv4Network(CLIENT_SUBNET, strict=False)
    host = random.randint(0, (1 << (32 - net.prefixlen)))
    return str(net.network_address + host)


def generate_access_log(i):
    now = datetime.now(timezone.utc)
    ts_ns = str(int(now.timestamp() * 1e9))

    ip = choose_client_ip()
    method = random.choice(METHODS)
    path = random.choice(PATHS)
    status = random.choice([200, 200, 200, 200, 500])
    size = random.randint(200, 1500)
    ua = random.choice(USER_AGENTS)

    # ✅ JSON log instead of plain text
    log_json = {
        "@timestamp": now.isoformat(),
        "client_ip": ip,
        "method": method,
        "path": path,
        "status": status,
        "response_size": size,
        "user_agent": ua,
        "app": "gateway",
        "job": "poc"
    }

    stream = {
        "stream": {
            "job": "poc",
            "app": "gateway",
        },
        "values": [[ts_ns, json.dumps(log_json)]]
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

        if r.status_code != 204 and r.status_code != 200:
            print(f"Error: {r.text}")

        time.sleep(0.1)


if __name__ == "__main__":
    push_logs()
