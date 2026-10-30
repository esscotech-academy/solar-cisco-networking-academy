# Module 01: Enterprise Networking Fundamentals & Protocol Mechanics

**Course**: Solar-Powered Cyber & Cisco Networking Academy  
**Organization**: ESSCO TECH AGENCY LTD (RC: 7192842)  
**Location**: Maiduguri, Borno State, Northeast Nigeria (Postal Code: 600282)  
**Target Certifications**: Cisco Certified Support Technician (CCST) Networking / CCNA 200-301  

---

## 1. Architectural Foundations: OSI vs. TCP/IP Models

Modern enterprise networks rely on layered abstraction to achieve vendor interoperability, deterministic packet traversal, and modular protocol design.

```
+-------------------------------------------------------------------+
|               OSI 7-LAYER VS. TCP/IP 4-LAYER MODEL                |
+---+----------------------+---+--------------------+---------------+
| # | OSI Layer Name       | # | TCP/IP Layer Name  | PDU Name      |
+---+----------------------+---+--------------------+---------------+
| 7 | Application          |   |                    |               |
| 6 | Presentation         | 4 | Application        | Data / Stream |
| 5 | Session              |   |                    |               |
+---+----------------------+---+--------------------+---------------+
| 4 | Transport            | 3 | Transport (Host)   | Segment (TCP) |
|   |                      |   |                    | Datagram(UDP) |
+---+----------------------+---+--------------------+---------------+
| 3 | Network              | 2 | Internet           | Packet        |
+---+----------------------+---+--------------------+---------------+
| 2 | Data Link (MAC/LLC)  | 1 | Network Access     | Frame         |
| 1 | Physical (PHY)       |   | (Link Layer)       | Bits          |
+---+----------------------+---+--------------------+---------------+
```

### 1.1 Encapsulation Deconstruction & Header Topologies

As an application payload transverses down the protocol stack, each layer prepends a protocol header (and in Layer 2, appends a frame check sequence trailer).

#### Ethernet II Frame Format (Layer 2)
```
+---------------+---------------+------------+-------------------+-------------+
| Preamble/SFD  | Dest MAC      | Src MAC    | EtherType (16-bit)| Payload     | FCS (CRC32) |
| (8 Bytes)     | (6 Bytes)     | (6 Bytes)  | 0x0800=IPv4       | (46-1500 B) | (4 Bytes)   |
|               |               |            | 0x86DD=IPv6       |             |             |
|               |               |            | 0x8100=802.1Q     |             |             |
+---------------+---------------+------------+-------------------+-------------+
```

#### IPv4 Header Anatomy (Layer 3 - 20 Bytes Minimum)
```
 0                   1                   2                   3
 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|Version|  IHL  |Type of Service|          Total Length         |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|         Identification        |Flags|      Fragment Offset    |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|  Time to Live |    Protocol   |        Header Checksum        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                       Source Address                          |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
|                    Destination Address                        |
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
```
* **Protocol Field Values**: `0x01` (ICMP), `0x06` (TCP), `0x11` (UDP), `0x59` (OSPF).
* **TTL (Time to Live)**: Decremented by 1 at every L3 hop; when it reaches 0, router drops packet and sends ICMP Type 11 (Time Exceeded) back to source.

---

## 2. Advanced IPv4 VLSM & Subnetting Mechanics

Variable Length Subnet Masking (VLSM) maximizes address space conservation by breaking subnets down recursively to match host density per broadcast domain.

### 2.1 The Subnet Engineering Formula Matrix

$$\text{Number of Subnets} = 2^s \quad (\text{where } s = \text{borrowed network bits})$$
$$\text{Usable Hosts per Subnet} = 2^h - 2 \quad (\text{where } h = \text{remaining host bits})$$
$$\text{Block Size (Magic Number)} = 256 - \text{Decimal Octet Value}$$

### 2.2 Academy Campus IP Address Plan (Base: `10.200.0.0/16`)

The Academy lab at Royas Plaza, Maiduguri requires logical separation between student workstation pods, instructor workstations, Cisco management interfaces, solar telemetry IoT nodes, and out-of-band serial consoles.

| Subnet Purpose | CIDR Prefix | Subnet Mask | Usable Host Range | Broadcast IP | Max Usable Hosts |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Solar Telemetry & BMS IoT** | `10.200.10.0/27` | `255.255.255.224` | `10.200.10.1` - `10.200.10.30` | `10.200.10.31` | 30 |
| **Network Infrastructure Mgmt** | `10.200.20.0/26` | `255.255.255.192` | `10.200.20.1` - `10.200.20.62` | `10.200.20.63` | 62 |
| **Student Pod A (Hardware)** | `10.200.30.0/24` | `255.255.255.0` | `10.200.30.1` - `10.200.30.254` | `10.200.30.255` | 254 |
| **Student Pod B (Virtual Labs)** | `10.200.31.0/24` | `255.255.255.0` | `10.200.31.1` - `10.200.31.254` | `10.200.31.255` | 254 |
| **Instructor & Exam Sandbox** | `10.200.40.0/25` | `255.255.255.128` | `10.200.40.1` - `10.200.40.126` | `10.200.40.127` | 126 |
| **Core WAN Point-to-Point 1** | `10.200.254.0/30`| `255.255.255.252` | `10.200.254.1` - `10.200.254.2` | `10.200.254.3` | 2 |
| **Core WAN Point-to-Point 2** | `10.200.254.4/30`| `255.255.255.252` | `10.200.254.5` - `10.200.254.6` | `10.200.254.7` | 2 |

---

## 3. IPv6 Architecture & Stateless Address Autoconfiguration (SLAAC)

IPv6 provides $2^{128}$ addresses, eliminating NAT in favor of end-to-end cryptographic visibility.

### 3.1 IPv6 Address Scopes & Allocation Rules
1. **Global Unicast Address (GUA)**: `2000::/3` (Publicly routable on the global Internet).
2. **Unique Local Address (ULA)**: `fc00::/7` (Private intranet routing, analogous to RFC 1918).
3. **Link-Local Address (LLA)**: `fe80::/10` (Mandatory on every IPv6 interface, non-routable beyond Layer 2 link, used for next-hop routing and neighbor discovery).
4. **Multicast**: `ff00::/8` (Replaces IPv4 broadcast entirely).
   - `ff02::1`: All IPv6 nodes on local link.
   - `ff02::2`: All IPv6 routers on local link.
   - `ff02::5`: All OSPFv3 routers.
   - `ff02::6`: All OSPFv3 Designated Routers (DR).

### 3.2 Modified EUI-64 Host ID Calculation
Converts a 48-bit MAC address into a 64-bit interface identifier:
1. Split MAC address in half: e.g., `00:1E:BD:54:A3:80` $\rightarrow$ `00:1E:BD` and `54:A3:80`.
2. Insert `FF:FE` in the middle: `00:1E:BD:FF:FE:54:A3:80`.
3. Invert the 7th bit (Universal/Local bit):
   - First byte `00` in binary is `0000 0000`.
   - Invert bit 7 $\rightarrow$ `0000 0010` (Hex `02`).
4. Final EUI-64 ID: `021e:bdff:fe54:a380`.
5. Link-Local Address: `fe80::021e:bdff:fe54:a380/64`.

---

## 4. Layer 2 Switching: VLANs, 802.1Q, & Spanning Tree (STP)

### 4.1 IEEE 802.1Q Frame Tagging & Native VLAN Security
To transport multiple broadcast domains over a single physical link, switches insert a 4-byte 802.1Q tag into the Ethernet frame header:
* **TPID (Tag Protocol Identifier)**: 16-bit value set to `0x8100`.
* **PCP (Priority Code Point)**: 3-bit CoS for QoS classification.
* **DEI (Drop Eligible Indicator)**: 1-bit drop eligibility during congestion.
* **VID (VLAN Identifier)**: 12-bit ID supporting 4,096 VLANs (VLAN 1-4094 usable).

```
   Original Frame:   [ Dest MAC ][ Src MAC ][ EtherType ][ Payload ][ FCS ]
   Tagged Frame:     [ Dest MAC ][ Src MAC ][ 802.1Q Tag ][ EtherType ][ Payload ][ FCS ]
                                             |-- 4 Bytes --|
```

> [!CAUTION] Native VLAN Hopping Vulnerability
> By default, frames on the Native VLAN traverse trunks untagged. If an attacker on an access port sends double-tagged 802.1Q frames, the first switch strips the outer tag (matching native VLAN) and forwards the inner tag to a victim VLAN. 
> **Defense**: Always change Native VLAN from default VLAN 1 to an unused dummy VLAN (e.g., VLAN 999), and force explicit tagging of native frames:
> ```ios
> vlan dot1q tag native
> ```

### 4.2 Spanning Tree Protocol (STP) Mechanics (IEEE 802.1D / 802.1w RSTP)
STP breaks Layer 2 loops caused by redundant physical links, preventing broadcast storms, multiple frame copies, and MAC database instability.

#### Root Bridge Election
The switch with the lowest **Bridge ID (BID)** becomes Root Bridge.
$$\text{Bridge ID} = \text{Bridge Priority (2 bytes)} + \text{System ID Extension (VLAN ID)} + \text{MAC Address (6 bytes)}$$
* Default Priority: `32768` (Configurable in increments of `4096`).
* Lowest Priority wins. If equal, lowest MAC address breaks the tie.

#### Port Roles in RSTP (802.1w)
* **Root Port (RP)**: The single port on a non-root switch with the lowest root path cost toward the Root Bridge.
* **Designated Port (DP)**: Port on a segment that sends the best BPDU. All ports on the Root Bridge are Designated.
* **Alternate Port (AP)**: Discarding port that provides an alternate path to the Root Bridge.
* **Backup Port (BP)**: Discarding port that provides redundant connection to the same segment.

#### STP Hardening Toolset
```ios
! Enable BPDU Guard on all access ports to drop rogue switches
spanning-tree portfast default
spanning-tree portfast bpduguard default

! Guard Root Bridge position against unauthorized high-priority switches
interface GigabitEthernet0/1
 spanning-tree guard root
```

---

## 5. Interior Gateway Routing: OSPFv2 (RFC 2328)

Open Shortest Path First (OSPF) is an open-standard, link-state routing protocol operating directly over IP (protocol 89).

### 5.1 Link-State Advertisements (LSAs) & SPF Computation
OSPF builds a complete topological database (LSDB) of the network. Every router runs Dijkstra's Shortest Path First (SPF) algorithm to calculate the loop-free shortest path tree:
$$\text{Cost} = \frac{\text{Reference Bandwidth}}{\text{Interface Bandwidth}}$$
* Cisco Default Reference Bandwidth: $10^8 \text{ bps}$ ($100 \text{ Mbps}$). In modern Gigabit networks, this must be adjusted:
```ios
router ospf 1
 auto-cost reference-bandwidth 100000  ! Normalizes reference to 100 Gbps
```

### 5.2 OSPF LSA Types Hierarchy

```
    +-----------------------------------------------+
    |             OSPF MULTI-AREA HIERARCHY         |
    |                                               |
    |   [ Area 10: Academic Pods ]                  |
    |         | (LSA Type 1, 2)                     |
    |      [ ABR Router ]                           |
    |         | (LSA Type 3 Summary)                |
    |   [ Area 0: Core Backbone ]                   |
    |         |                                     |
    |      [ ASBR Router ]                          |
    |         | (LSA Type 4, 5 External)            |
    |     [ Internet / Starlink Uplink ]            |
    +-----------------------------------------------+
```

* **Type 1 (Router LSA)**: Generated by every router, describing its local links and states. Stays within its originating area.
* **Type 2 (Network LSA)**: Generated by the Designated Router (DR) on multiaccess segments. Stays within originating area.
* **Type 3 (Summary LSA)**: Generated by Area Border Routers (ABRs) to summarize networks from one area into another.
* **Type 4 (ASBR Summary LSA)**: Generated by ABRs to advertise how to reach an Autonomous System Boundary Router (ASBR).
* **Type 5 (External LSA)**: Generated by ASBRs to advertise routes redistributed from external sources (e.g., BGP or static default routes).

### 5.3 OSPF Adjacency State Machine
To form an adjacency, two neighbors must transition through 7 states:
1. **Down**: No OSPF hello packets received.
2. **Init**: Received Hello from neighbor, but local Router ID not seen in neighbor's list.
3. **2-Way**: Bidirectional communication confirmed. DR/BDR election occurs on broadcast networks.
4. **ExStart**: Master/Slave relationship established via Database Description (DBD) packets to determine sequence numbers.
5. **Exchange**: Routers exchange DBD packets describing their LSDB summaries.
6. **Loading**: Routers send Link-State Requests (LSR) and receive Link-State Updates (LSU) with full LSAs.
7. **Full**: LSDBs are fully synchronized. Routing table populated via SPF.

---

## 6. End-of-Module Review Questions & Practical Challenge

1. **Subnetting Calculation**: You are assigned `10.200.128.0/22`. Carve out two subnets of at least 120 hosts for Pod C and Pod D, and four point-to-point subnets (`/30`) for router serial uplinks. Document the network, usable host range, and broadcast address for each.
2. **STP Root Port Analysis**: Switch A has MAC `0000.0000.1111` and Priority `32768`. Switch B has MAC `0000.0000.2222` and Priority `4096`. Which switch is Root Bridge? If Switch A has two Gigabit links to Switch B, how does Switch A pick its Root Port?
3. **OSPF Multi-Area Troubleshooting**: An engineer configures Area 20 without a physical connection to Area 0. Will routes from Area 20 appear in Area 10? What Cisco feature can solve this if a direct physical link cannot be run?
