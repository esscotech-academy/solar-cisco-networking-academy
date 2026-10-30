# Security Policy

## Overview
The **Solar-Powered Cyber & Cisco Networking Academy (Northeast Nigeria)** is operated by **ESSCO TECH AGENCY LTD (RC: 7192842)** at Royas Plaza, Damboa Road, Maiduguri, Borno State (Postal Code: 600282).

Because this project combines open educational assets, production Cisco network hardware templates, IoT solar microgrid telemetry, and defensive cybersecurity operations in an off-grid regional infrastructure deployment, maintaining the highest standard of infrastructure security is mission-critical.

---

## Supported Versions

Only the latest commit on the `main` branch of this repository receives security updates and patches.

| Component / Subsystem | Supported Version | Status |
| :--- | :--- | :--- |
| `automation/cisco_backup_engine.py` | v1.0.x / `main` | :white_check_mark: Actively Supported |
| `automation/solar_telemetry_daemon.py` | v1.0.x / `main` | :white_check_mark: Actively Supported |
| `labs/` (Cisco IOS & Snort) | Current Templates | :white_check_mark: Actively Supported |
| `curriculum/` | Current Release | :white_check_mark: Actively Supported |

---

## Reporting a Vulnerability

We deeply appreciate and welcome responsible disclosure from independent security researchers, network engineers, and community auditors.

### 1. Private Disclosure Channel
**Do NOT file public GitHub issues for security vulnerabilities.**

Instead, report vulnerabilities privately by sending an encrypted or cleartext email to our dedicated security response team:

* **Primary Email**: `security@esscotechagency.com`
* **Alternate Escalation**: `governance@esscotechagency.com`
* **Subject Line**: `[SECURITY VULNERABILITY] <Component>: <Brief Description>`

### 2. Report Information Needed
To help us triage and remediate the issue rapidly, please include:
1. Exact component(s) affected (e.g., `solar_telemetry_daemon.py`, specific Cisco IOS template).
2. Detailed description of the vulnerability and its potential impact.
3. Proof-of-Concept (PoC) code or step-by-step reproduction instructions.
4. Suggested remediation or patch (if available).
5. Your name/handle for attribution in our release security advisories.

### 3. Response & Remediation SLA
* **Initial Acknowledgment**: Within **24 to 48 hours**.
* **Triage & Impact Assessment**: Within **72 hours**.
* **Remediation & Patch Deployment**: Within **7 to 14 business days** (depending on severity).
* **Public Advisory**: Published concurrently with the patch, adhering to a 90-day responsible disclosure window.

---

## Threat Model & Physical Realities

When evaluating the security of this repository's assets, keep in mind our real-world threat model in Borno State:

1. **Hostile Electromagnetic & Physical Environment**:
   - The academy operates in an environment subject to extreme municipal power instability, extended utility outages, and electrical surges.
   - All management interfaces must be strictly isolated to out-of-band management VLANs.
2. **Defensive Isolation**:
   - The lab network is physically and logically partitioned from public student Wi-Fi and production agency servers.
   - All student lab exercises take place within non-routable RFC 1918 segments monitored by IDS/IPS (Snort) engines.
3. **Telemetry & Microgrid Integrity**:
   - Solar telemetry communicates over authenticated SNMPv3 or isolated local serial/Modbus channels.
   - The automatic load-shedding daemon enforces strict input validation to prevent false-positive command execution that could take down core uplinks.

---

## Ethical Bounds for Students & Researchers

1. **Authorization**: Testing of offensive tools is strictly confined to air-gapped virtual sandboxes (GNS3 / EVE-NG / dedicated test pods).
2. **No External Scanning**: Students and contributors are prohibited from directing scanning, probing, or denial-of-service traffic at upstream satellite (Starlink), cellular ISP (MTN/Airtel), or local institutional infrastructure.
3. **Open Educational Mandate**: All defensive rules and forensics guides are created to protect civic society, educational facilities, and critical enterprise infrastructure across Northeast Nigeria.
