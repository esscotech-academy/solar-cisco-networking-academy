# Contributing to the Solar-Powered Cyber & Cisco Networking Academy

Thank you for your interest in contributing to the **Solar-Powered Cyber & Cisco Networking Academy (Northeast Nigeria)**, operated by **ESSCO TECH AGENCY LTD (RC: 7192842)**.

This repository serves as both an Open Educational Resource (OER) for marginalized youth and women in Maiduguri, Borno State, and a production-grade infrastructure blueprint for ruggedized off-grid network engineering. We welcome high-rigor contributions from network architects, security researchers, systems programmers, and educational designers worldwide.

---

## Table of Contents
1. [Code of Conduct](#code-of-conduct)
2. [Guiding Principles & Ethical Standards](#guiding-principles--ethical-standards)
3. [Development Environment Setup](#development-environment-setup)
4. [Contribution Workflow](#contribution-workflow)
5. [Engineering Standards](#engineering-standards)
   - [Cisco IOS Configurations](#cisco-ios-configurations)
   - [Snort IDS Rules](#snort-ids-rules)
   - [Python Network Automation](#python-network-automation)
   - [Curriculum & Documentation](#curriculum--documentation)
6. [Testing & CI Gates](#testing--ci-gates)
7. [Submitting Pull Requests](#submitting-pull-requests)

---

## Code of Conduct
All contributors are expected to uphold our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat all participants with respect and professional empathy.

---

## Guiding Principles & Ethical Standards

1. **Defensive Operations Only**: All cybersecurity labs, telemetry rules, and packet analysis material must focus strictly on **defensive security (Blue Team)**, threat detection, infrastructure resilience, and audit compliance. No weaponized exploits, offensive attack tools, or malicious payloads are permitted.
2. **Deterministic, Production-Ready Code**: No pseudo-code or placeholder implementations. Every script must run cleanly with proper error handling, logging, and typing.
3. **Bandwidth & Energy Constrained Realities**: Remember that these tools run in Maiduguri under high ambient temperatures (35°C–44°C), intermittent solar battery power, and satellite/cellular uplink constraints. Code must be lightweight, resilient to network drops, and resource-conscious.

---

## Development Environment Setup

### Prerequisites
* Python 3.10, 3.11, or 3.12
* Git 2.30+
* Virtual environment tool (`venv`)
* Recommended: VS Code, Wireshark, Cisco Packet Tracer 8.2+ or GNS3/EVE-NG

### Local Setup
```bash
# Clone your fork
git clone https://github.com/<your-username>/solar-cisco-networking-academy.git
cd solar-cisco-networking-academy

# Create and activate a virtual environment
python -m venv .venv

# On Linux/macOS:
source .venv/bin/activate
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Install runtime and testing dependencies
pip install --upgrade pip
pip install -r automation/requirements.txt
pip install flake8 black mypy pytest
```

---

## Contribution Workflow

We follow the standard GitHub Flow model with Conventional Commits:

```
main ────┬───────────────────────────────┬───>
         └── feat/snort-dns-rules ───────┘
```

### 1. Branch Naming Conventions
* `feat/<short-description>`: New curriculum module, lab, or automation tool
* `fix/<short-description>`: Bug fix in Python scripts or correction in IOS templates
* `docs/<short-description>`: Documentation, BOM update, or curriculum refinement
* `ci/<short-description>`: GitHub Actions workflow updates

### 2. Commit Message Standards (Conventional Commits)
Format: `<type>(<scope>): <subject>`

Examples:
* `feat(telemetry): add hysteresis loop to prevent battery switchport flapping`
* `fix(cisco-ios): correct VTY access-class direction in hardening template`
* `docs(curriculum): expand OSPFv2 LSA Type 3/4 explanation for multi-area lab`
* `test(backup): add mock netmiko transport tests for CI pipeline`

---

## Engineering Standards

### Cisco IOS Configurations
* **No Plaintext Credentials**: Never commit unhashed passwords. Use `enable algorithm-type scrypt` or `secret` with SHA-256 where supported, or standard Cisco type 5/8/9 hashes.
* **RFC 1918 Private Addressing**: All lab configurations must strictly use RFC 1918 private address ranges (`10.0.0.0/8`, `172.16.0.0/12`, or `192.168.0.0/16`) or RFC 5737 documentation blocks (`192.0.2.0/24`, `198.51.100.0/24`, `203.0.113.0/24`).
* **Explicit Administrative State**: Always state interface administrative status (`shutdown` or `no shutdown`).
* **Management Security**: Every switch/router configuration must enforce SSHv2, AAA authentication, login delay/block-for brute force protection, and disable unsecure protocols (Telnet, HTTP server).

### Snort IDS Rules
* Must conform to standard Snort 2.9 / 3.x syntax.
* Must include mandatory options: `msg`, `sid` (use custom range 1,000,001+), `rev`, and `classtype`.
* Must specify protocol, direction (`->` or `<>`), and port ranges accurately.
* Must be validated against the automated CI linter.

### Python Network Automation
* **Typing**: Use PEP 484 type annotations for all function parameters and return types.
* **Data Models**: Use `pydantic` v2 for schema validation, device inventories, and telemetry metrics.
* **Resilience**: Every network connection via `netmiko` or `pysnmp` must catch timeout and authentication errors (`NetmikoTimeoutException`, `NetmikoAuthenticationException`, etc.) and log them clearly using `rich.logging` or Python's standard `logging` library.
* **Mock Capability**: Any script interacting with physical network devices must supply a `--mock` or `--dry-run` flag so it can be verified in automated CI without hardware present.
* **Style**: Code must pass `black --check` (120 char line limit) and `flake8`.

### Curriculum & Documentation
* Written in clear, precise technical English.
* Include ASCII or Mermaid diagrams where conceptual topologies, packet headers, or state transitions are explained.
* Adhere to Cisco Certified Support Technician (CCST), CCNA 200-301, and Cisco CyberOps Associate exam objectives.

---

## Testing & CI Gates

Before opening a Pull Request, run the local validation checks:

```bash
# 1. Format code
black automation/

# 2. Lint Python
flake8 automation/ --max-line-length=120

# 3. Dry-run automation tools
python automation/cisco_backup_engine.py --dry-run --mock
python automation/solar_telemetry_daemon.py --mock --iterations 2 --interval 1

# 4. Verify Snort rule syntax
python -c "
import re
with open('labs/lab-03-snort-threat-detection.rules') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#'):
            assert re.match(r'^\w+\s+\w+\s+\S+\s+\S+\s+(->|<>)\s+\S+\s+\S+\s+\(.*\)$', line), f'Invalid: {line}'
print('Snort rules valid!')
"
```

---

## Submitting Pull Requests

1. Push your branch to your fork.
2. Open a Pull Request against `main` on the primary repository.
3. Complete the PR template description:
   - What problem does this PR solve?
   - How was it tested?
   - Does this introduce any breaking changes to the hardware BOM or lab topologies?
4. Ensure all GitHub Actions status checks pass.
5. Academy maintainers will review your PR within 48–72 hours.

Thank you for investing in the future of West African infrastructure engineering!
