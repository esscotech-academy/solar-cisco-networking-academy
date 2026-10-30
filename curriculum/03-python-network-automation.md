# Module 03: Python Network Automation & Programmability

**Course**: Solar-Powered Cyber & Cisco Networking Academy  
**Organization**: ESSCO TECH AGENCY LTD (RC: 7192842)  
**Location**: Maiduguri, Borno State, Northeast Nigeria (Postal Code: 600282)  
**Target Certifications**: Cisco Certified DevNet Associate (DEVASC 200-901) / CCNA Automation Objectives  

---

## 1. Why Automation Matters in Remote & Off-Grid Infrastructure

In Northeast Nigeria, network administrators face unique operational constraints:
* **Severe Energy Scarcity**: Labs operate on finite LiFePO4 battery banks; manual CLI administration during grid failures wastes battery power and technician time.
* **Intermittent Uplinks**: Starlink and cellular data links can experience rain-fade or bandwidth throttling; automated scheduled routines push batched configuration changes in seconds rather than hours of interactive terminal sessions.
* **Human Error Elimination**: Manual configuration changes on remote edge routers can accidentally sever the only management pathway, necessitating costly on-site technician dispatch across dispersed rural sites.

Python network automation transforms infrastructure from manual craft to deterministic, version-controlled software.

---

## 2. Python SSH Automation Architecture: Netmiko Deep Dive

While low-level libraries like `paramiko` provide raw SSH protocol bindings, [Netmiko](https://github.com/ktbyers/netmiko) (built on Paramiko by Kirk Byers) abstracts multi-vendor CLI quirks:
* Handling terminal pagination (`--More--` prompts).
* Entering and verifying `enable` privilege mode.
* Command prompt synchronization and timing delays.
* Vendor-specific syntax escaping (Cisco IOS, Arista EOS, Juniper Junos).

```
+--------------------------------------------------------------------+
|                  NETMIKO ARCHITECTURAL STACK                       |
|                                                                    |
|  [ Academy Application Code: cisco_backup_engine.py ]              |
|                             │                                      |
|                             ▼                                      |
|  [ Netmiko: CiscoIosBase (Handles prompts, pagination, # enable) ] |
|                             │                                      |
|                             ▼                                      |
|  [ Paramiko: SSHv2 Transport, Cryptographic Key Exchange, Channels]|
|                             │                                      |
|                             ▼                                      |
|  [ Python Sockets: TCP Port 22 / Encrypted Transport ]            |
+--------------------------------------------------------------------+
```

### 2.1 Establishing Resilient Connections with Netmiko

```python
from netmiko import ConnectHandler
from netmiko.exceptions import (
    NetmikoTimeoutException,
    NetmikoAuthenticationException,
)

cisco_device = {
    "device_type": "cisco_ios",
    "host": "10.200.20.1",
    "username": "netadmin",
    "password": "SecurePassword123!",
    "secret": "EnableSecretScrypt!",
    "fast_cli": False,            # Set False on older Catalyst 2960/3560 CPUs
    "timeout": 15,                # Accommodate satellite latency jitter
    "global_delay_factor": 1.5,   # Adjust timing for low-power switches
}

try:
    print(f"Connecting to {cisco_device['host']}...")
    with ConnectHandler(**cisco_device) as net_connect:
        net_connect.enable()
        prompt = net_connect.find_prompt()
        print(f"Successfully authenticated. Device prompt: {prompt}")

        # Execute safe operational command
        version_output = net_connect.send_command("show version | include uptime")
        print(f"System Uptime: {version_output.strip()}")

except NetmikoTimeoutException:
    print(f"CRITICAL: Connection timed out to {cisco_device['host']}. Check physical link or solar power.")
except NetmikoAuthenticationException:
    print(f"CRITICAL: Authentication failed for {cisco_device['username']}@{cisco_device['host']}.")
except Exception as exc:
    print(f"UNHANDLED ERROR: {exc}")
```

### 2.2 Pushing Structured Configurations (`send_config_set`)

Unlike `send_command` (which runs in user or enable exec mode), `send_config_set` automatically enters global configuration mode (`configure terminal`), applies an array of commands, verifies execution without errors, and exits back to enable mode.

```python
hardening_commands = [
    "service password-encryption",
    "ip ssh version 2",
    "ip ssh time-out 60",
    "ip ssh authentication-retries 3",
    "login block-for 180 attempts 3 within 60",
]

with ConnectHandler(**cisco_device) as conn:
    conn.enable()
    output = conn.send_config_set(hardening_commands)
    # Persist running configuration to NVRAM
    save_output = conn.save_config()
    print("Configuration deployed and saved.")
```

---

## 3. Modern Network Programmability: RESTCONF & YANG Data Models

Modern enterprise networks (Cisco IOS-XE 16.x+, Catalyst 9000) support programmatic API interaction via **RESTCONF** (RFC 8040) using structured JSON or XML over HTTPS, modeled with **YANG** (RFC 7950).

```
   HTTP Verb    CRUD Action    RESTCONF Equivalent
   ---------    -----------    -------------------
   GET          Read           Retrieve operational/configuration data
   POST         Create         Create a new child resource
   PUT          Replace        Replace an entire resource
   PATCH        Update         Merge/modify specific attributes
   DELETE       Delete         Remove a resource
```

### 3.1 Fetching Interface Telemetry with Python `requests`

```python
import requests
import json
from requests.auth import HTTPBasicAuth

# Suppress self-signed certificate warnings in lab sandbox
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DEVICE_IP = "10.200.20.1"
RESTCONF_PORT = 443
URL = f"https://{DEVICE_IP}:{RESTCONF_PORT}/restconf/data/ietf-interfaces:interfaces"

headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json",
}

response = requests.get(
    URL,
    headers=headers,
    auth=HTTPBasicAuth("netadmin", "SecurePassword123!"),
    verify=False,
    timeout=10,
)

if response.status_code == 200:
    interfaces_data = response.json()
    print(json.dumps(interfaces_data, indent=2))
else:
    print(f"RESTCONF query failed with status code {response.status_code}: {response.text}")
```

---

## 4. Configuration Drift Detection via Python `difflib`

Configuration drift occurs when unauthorized manual changes are made to network hardware outside established change management procedures.

The academy backup daemon (`automation/cisco_backup_engine.py`) employs Python's built-in `difflib` and cryptographic hashing (`hashlib.sha256`) to flag unauthorized drift immediately.

### Drift Detection Logic

```python
import difflib
import hashlib

def calculate_hash(config_text: str) -> str:
    """Compute SHA-256 hash of normalized configuration string."""
    normalized = "\n".join([line.strip() for line in config_text.splitlines() if line.strip() and not line.startswith("!")])
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()

def detect_drift(baseline_config: str, running_config: str) -> list[str]:
    """Generate unified diff showing additions and deletions."""
    baseline_lines = baseline_config.splitlines(keepends=True)
    running_lines = running_config.splitlines(keepends=True)

    diff = list(difflib.unified_diff(
        baseline_lines,
        running_lines,
        fromfile="golden-baseline.cfg",
        tofile="current-running.cfg",
        n=2,
    ))
    return diff
```

---

## 5. Lab Challenge: Build an Automated Device Auditor

Students in this module develop an automated auditor script that:
1. Queries the academy switch inventory concurrently using `concurrent.futures`.
2. Inspects `show ip interface brief` to detect any rogue ports active in VLAN 1.
3. Automatically triggers an alert if unauthorized MAC addresses appear on port-security violation counters.
4. Generates an executive HTML report stored on the local academy intranet dashboard.
