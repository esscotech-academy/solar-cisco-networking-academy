# Module 02: Defensive Cybersecurity, Threat Hunting & Packet Forensics

**Course**: Solar-Powered Cyber & Cisco Networking Academy  
**Organization**: ESSCO TECH AGENCY LTD (RC: 7192842)  
**Location**: Maiduguri, Borno State, Northeast Nigeria (Postal Code: 600282)  
**Target Certifications**: Cisco Certified Support Technician (CCST) Cybersecurity / Cisco CyberOps Associate  

---

## 1. Enterprise Linux System Hardening Runbook

Defensive engineering begins at the operating system layer. Academy lab servers and student workstations running Debian GNU/Linux 12 (Bookworm) are hardened according to the Center for Internet Security (CIS) Level 2 benchmark.

### 1.1 Kernel Networking Hardening (`/etc/sysctl.d/99-security.conf`)

By tuning kernel parameters through `sysctl`, we drop malformed packets, mitigate SYN floods, and eliminate Man-in-the-Middle (MitM) ICMP redirect vectors at the kernel level before they reach userspace:

```ini
# Disable IP Forwarding (Ensure machine does not act as unauthorized router)
net.ipv4.ip_forward = 0
net.ipv6.conf.all.forwarding = 0

# Mitigate IP Spoofing (Enable Reverse Path Filtering - RFC 3704)
net.ipv4.conf.all.rp_filter = 1
net.ipv4.conf.default.rp_filter = 1

# Ignore ICMP Echo Broadcasts (Smurf Attack Mitigation)
net.ipv4.icmp_echo_ignore_broadcasts = 1

# Ignore Bogus ICMP Error Responses
net.ipv4.icmp_ignore_bogus_error_responses = 1

# Disable ICMP Redirect Acceptance (Mitigates Route Injection MitM)
net.ipv4.conf.all.accept_redirects = 0
net.ipv4.conf.default.accept_redirects = 0
net.ipv4.conf.all.secure_redirects = 0
net.ipv4.conf.default.secure_redirects = 0
net.ipv6.conf.all.accept_redirects = 0
net.ipv6.conf.default.accept_redirects = 0

# Do Not Send ICMP Redirects
net.ipv4.conf.all.send_redirects = 0
net.ipv4.conf.default.send_redirects = 0

# Enable TCP SYN Cookies (SYN Flood Denial of Service Defense)
net.ipv4.tcp_syncookies = 1
net.ipv4.tcp_max_syn_backlog = 4096
net.ipv4.tcp_synack_retries = 2

# Log Martians (Packets with Impossible Source Addresses)
net.ipv4.conf.all.log_martians = 1
net.ipv4.conf.default.log_martians = 1

# Disable Source Packet Routing
net.ipv4.conf.all.accept_source_route = 0
net.ipv6.conf.all.accept_source_route = 0
```

Apply immediately without reboot:
```bash
sudo sysctl --system
```

### 1.2 Enterprise OpenSSH Hardening (`/etc/ssh/sshd_config.d/hardening.conf`)

Remote administrative access is restricted to modern elliptic curve cryptography:

```text
# Port and Protocol
Port 2222
Protocol 2

# Cryptographic Key Exchange & Ciphers
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group16-sha512
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com
MACs hmac-sha2-512-etm@openssh.com

# Authentication Restrictions
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AuthenticationMethods publickey
MaxAuthTries 3
LoginGraceTime 30
PermitEmptyPasswords no
X11Forwarding no
MaxSessions 2
ClientAliveInterval 300
ClientAliveCountMax 0

# Allow specific administrative group only
AllowGroups academy-netadmins
```

---

## 2. Wireshark Packet Forensics & Protocol Anomaly Analysis

Network traffic analysis allows defense analysts to identify hostile activity without relying on signatures.

### 2.1 ARP Cache Poisoning (Man-in-the-Middle) Detection
Attackers use tools like Ettercap or Arpspoof to overwrite the MAC tables of victim workstations and default gateways by sending unsolicited Gratuitous ARP (GARP) replies.

```
Attacker (10.200.30.55 | MAC: 00:0C:29:AA:BB:CC)
   ├─── [ARP Reply: 10.200.30.1 is at 00:0C:29:AA:BB:CC] ───> Victim (10.200.30.100)
   └─── [ARP Reply: 10.200.30.100 is at 00:0C:29:AA:BB:CC] ─> Gateway (10.200.30.1)
```

#### Wireshark Display Filter
```wireshark
arp.duplicate-address-frame or (arp.opcode == 2 and eth.src != 00:1e:bd:54:a3:80)
```
* **Forensic Indicators**:
  1. Multiple distinct MAC addresses claiming ownership of the default gateway IP (`10.200.30.1`).
  2. High frequency of ARP Reply packets without corresponding preceding ARP Request packets (`arp.opcode == 2`).
  3. Cisco Switch Symptom: `%SW_DAI-4-DHCP_SNOOPING_DENY` or `%MAC_MOVE` syslog alerts.

### 2.2 TCP SYN Flood Analysis
In a SYN flood attack, an adversary transmits rapid streams of TCP SYN requests from spoofed IP addresses, forcing the target server to allocate half-open state structures in its socket backlog until connection exhaustion occurs.

#### Wireshark Display Filter
```wireshark
tcp.flags.syn == 1 and tcp.flags.ack == 0 and tcp.window_size <= 1024
```
* **Forensic Indicators**:
  1. High volume of TCP SYN packets directed at a single destination port (e.g. 80, 443, 22) with zero completion of the three-way handshake (`SYN-ACK` received, but no concluding `ACK`).
  2. Random source IP distribution with non-routable or unallocated addresses.
  3. Server socket state inspectable via terminal: `ss -t -a | grep -i syn-recv`.

### 2.3 DNS Exfiltration & Tunneling Detection
Adversaries bypass perimeter firewalls by encapsulating files or command-and-control (C2) payloads within Base64-encoded subdomains queried against an attacker-controlled authoritative name server.

```
Victim Box ──> DNS Query: "dGhpcy1pcy1hLXNlY3JldC1rZXkK.attacker-c2.net" (Type: TXT) ──> Ext NS
```

#### Wireshark Display Filter
```wireshark
dns.qry.name.len > 50 or dns.resp.len > 512 or dns.qry.type == 16
```
* **Forensic Indicators**:
  1. Subdomain length exceeding 45–60 characters.
  2. Shannon entropy scores above 3.8 in query labels (indicating encrypted/compressed payloads rather than human-readable hostnames).
  3. Abnormally high volume of `TXT` or `NULL` DNS record types compared to standard `A`/`AAAA` lookups.

---

## 3. Snort Intrusion Detection System (IDS) Engine

Snort is an open-source Network Intrusion Detection System (NIDS) capable of real-time traffic analysis and packet logging.

### 3.1 Anatomy of a Production Snort Rule

```
   +----------------- Rule Header ------------------+ +------------- Rule Options ---------------+
   alert tcp $EXTERNAL_NET any -> $HOME_NET 22        (msg:"SCAN Nmap SSH Scan"; flags:S; sid:1000001; rev:1;)
   |---| |-| |-----------| |-| || |-------| |--|       |-----------------------------------------------------|
     |    |        |        |   |     |      |                                   |
   Action |    Source IP   Port |  Dest IP  Port                               Body / Options
       Protocol              Direction
```

#### Rule Header Components
* **Action**: `alert`, `log`, `drop`, `reject`, `pass`.
* **Protocol**: `tcp`, `udp`, `icmp`, `ip`.
* **Direction**: `->` (Unidirectional) or `<>` (Bidirectional).

#### Critical Rule Options
* `msg`: Human-readable description emitted in alerts.
* `content`: Exact string or binary sequence to match (e.g., `content:"|00 01 86 a5|"`, `content:"/etc/passwd"`).
* `nocase`: Case-insensitive string matching.
* `depth` & `offset`: Specify byte offsets for pattern searching within the payload.
* `distance` & `within`: Relative search parameters chained after a previous content match.
* `threshold`: Rate-limiting directive (e.g. `type limit, track by_src, count 1, seconds 60`).
* `sid`: Snort Rule ID. Reserved ranges:
  - `< 100`: Reserved by system.
  - `100 - 999,999`: Official Snort rule sets.
  - `1,000,000+`: Local and custom user-defined rules.
* `rev`: Revision integer, incremented with each rule alteration.
* `classtype`: Categorizes alert severity (`attempted-admin`, `bad-traffic`, `scan-detection`, etc.).

---

## 4. MITRE ATT&CK Framework Mapping Matrix

The Academy curriculum structures all defensive hunting exercises around the global **MITRE ATT&CK Enterprise Matrix**:

| MITRE Technique ID | Technique Name | Attack Description | Academy Defensive Countermeasure |
| :--- | :--- | :--- | :--- |
| **T1046** | Network Service Discovery | Adversary executes Nmap TCP SYN/NULL/XMAS scans across subnets. | Snort rule `sid:1000001`, Dynamic ARP Inspection, Cisco VTY ACLs. |
| **T1110.001** | Password Guessing / Brute Force | Repeated SSH / Telnet authentication attempts against switches or Linux boxes. | `login block-for 180 attempts 3 within 60`, PAM `faillock`, Snort threshold rule. |
| **T1059.004** | Unix Shell Command Execution | Web-based command injection spawning `/bin/sh` or `/bin/bash`. | Snort rule `sid:1000009`, Linux `auditd` process exec rules, AppArmor profiles. |
| **T1071.004** | DNS Application Layer Protocol | DNS exfiltration / C2 tunneling bypassing L4 egress filters. | Snort high-entropy rule `sid:1000006`, local Pi-hole/Unbound logging and sinkholing. |
| **T1498.001** | Network DoS: Direct Flooding | High-velocity SYN or UDP flood designed to exhaust lab uplink. | Kernel SYN cookies (`net.ipv4.tcp_syncookies=1`), Cisco CoPP (Control Plane Policing). |

---

## 5. Defensive Hands-On Exercise: Analyzing a Live Intrusion

In the accompanying lab `labs/lab-03-snort-threat-detection.rules`, students deploy custom detection logic into an active monitoring container.

### Exercise Scenario
An unauthorized node on VLAN 30 (`10.200.30.99`) attempts an SSH brute-force attack against the primary Cisco Catalyst 3560 switch (`10.200.20.1`).

1. **Verify Detection Rule**:
   ```snort
   alert tcp $EXTERNAL_NET any -> $HOME_NET 22 (msg:"SECURITY ALERT: SSH Brute Force Rate Exceeded"; flow:to_server,established; content:"SSH-"; threshold:type both, track by_src, count 5, seconds 30; classtype:attempted-admin; sid:1000002; rev:1;)
   ```
2. **Execute Detection Test**:
   Run Snort against the capture interface in console alert mode:
   ```bash
   sudo snort -A console -q -u snort -g snort -c /etc/snort/snort.conf -i eth1
   ```
3. **Validate Incident Log**:
   When triggered, parse the structured alert log in `/var/log/snort/alert` to identify attacker MAC, IP, and timestamp.
