# Engineering Bill of Materials (BOM) & Microgrid Architecture

**Facility**: Solar-Powered Cyber & Cisco Networking Academy  
**Operating Entity**: ESSCO TECH AGENCY LTD (RC: 7192842)  
**Location**: Royas Plaza, Damboa Road, Maiduguri, Borno State, Nigeria (Postal Code: 600282)  
**System Rating**: 10.2 kWp Photovoltaic Generation / 28.8 kWh LiFePO4 Storage / 10 kW Continuous AC Output  

---

## 1. System Design Rationale & Regional Operating Conditions

Maiduguri experiences extreme seasonal temperature swings (35°C–44°C ambient during hot season), intense solar irradiance (average 6.2–6.8 peak sun hours/day), and prolonged periods of municipal grid instability across the regional electrical distribution network. Additionally, fine airborne Saharan silica dust (Harmattan season, November–February) requires specialized positive-pressure air filtration and IP54/IP65 equipment ratings.

To ensure uninterrupted vocational training for 100 students annually across two shifts, the lab is engineered with an autonomous, DC-coupled solar microgrid providing 100% sovereign power autonomy.

---

## 2. Comprehensive Bill of Materials

### 2.1 Solar Photovoltaic Generation Subsystem
| Item # | Component Description | Manufacturer & Model | Qty | Unit Spec / Rating | Total Capacity | Unit Cost (USD) | Extended (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PV-01** | Tier-1 Monocrystalline Bifacial Half-Cell Solar Panels | Jinko Solar Tiger Pro 545W / Longi Hi-MO 5 | 20 | 545 Wp, Voc 49.5V, Isc 13.9A, 21.3% Eff | 10.90 kWp | $145.00 | $2,900.00 |
| **PV-02** | Anodized Aluminum Ground & Ballasted Roof Racking | Schletter / Clenergy Solar Terraground | 1 | 25° Tilt, Galvanized Steel Stanchions, 140km/h wind | -- | $1,200.00 | $1,200.00 |
| **PV-03** | 6-String DC Array Combiner Box with Class II SPDs | Suntree IP65 Combiner (1000V DC, 15A fuses, Type 2 SPD) | 2 | Dual MPPT input arrays, 1000V DC 40kA surge arresters | -- | $280.00 | $560.00 |
| **PV-04** | UV-Resistant Double-Insulated Solar PV DC Cable (6mm²) | Helukabel Solarflex-X PV1-F (Halogen-Free) | 300m | 6mm² Tinned Copper, 1.5kV DC rated | -- | $1.20/m | $360.00 |
| **PV-05** | MC4 IP68 Locking Connectors & Y-Branch Combiners | Staubli Multi-Contact Original MC4 | 24 pr | 1000V DC, 30A, UL94-V0 flame retardant | -- | $3.50 | $84.00 |

### 2.2 Power Conversion & Energy Storage Subsystem
| Item # | Component Description | Manufacturer & Model | Qty | Unit Spec / Rating | Total Capacity | Unit Cost (USD) | Extended (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **PWR-01**| Low-Voltage 48V Pure Sine Wave Hybrid Inverter | Deye SUN-10K-SG02LP1-EU-AM3 / Victron MultiPlus-II | 1 | 10,000W Continuous, Dual MPPT (500V max), 220V/50Hz | 10.0 kW | $2,650.00 | $2,650.00 |
| **PWR-02**| Server-Rack 48V 100Ah LiFePO4 Battery Modules | Pylontech US5000 / Dyness A48100 (15S / 16S BMS) | 6 | 4.8 kWh nominal per pack, 6000 cycles @ 80% DoD | 28.8 kWh | $1,350.00 | $8,100.00 |
| **PWR-03**| Standard 19" 12U Reinforced Heavy-Duty Battery Cabinet | Toten Modular Battery Rack (500kg static load) | 1 | Welded steel, integrated DC busbars & ground straps | -- | $380.00 | $380.00 |
| **PWR-04**| 250A 48V DC Battery Disconnect Switch & NH1 Fuses | Jean Müller / Bussmann 250A gPV Fused Isolator | 1 | Dual pole DC disconnect, 25kA breaking capacity | -- | $220.00 | $220.00 |
| **PWR-05**| Microgrid Smart Shunt & IoT Telemetry Gateway | Victron SmartShunt 500A/50mV & Cerbo GX Telemetry | 1 | Modbus TCP, VE.Can, Bluetooth, RS485 to ESP32 | -- | $390.00 | $390.00 |

### 2.3 AC Electrical Distribution & Surge Suppression
| Item # | Component Description | Manufacturer & Model | Qty | Unit Spec / Rating | Total Capacity | Unit Cost (USD) | Extended (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **AC-01** | Main Distribution Panelboard (MDB) with Automatic Transfer | Schneider Electric Acti9 Isobar 24-Way Board | 1 | 63A 2-Pole Mains, 30mA RCD protection | -- | $420.00 | $420.00 |
| **AC-02** | Type 1+2 Combined Lightning & Surge Protection Device (SPD)| Dehn / Hager Type 1+2 TT/TN-S (Iimp 12.5kA, Up < 1.5kV) | 2 | Essential for Maiduguri thunderstorm surge protection | -- | $290.00 | $580.00 |
| **AC-03** | Individual Branch MCBs (Type C for inductive IT loads) | Schneider Acti9 iC60N 10A / 16A 1-Pole Breakers | 16 | 6kA breaking capacity | -- | $9.50 | $152.00 |
| **AC-04** | Solid Copper Earth Ground Rods & Chemical Backfill | 5/8" x 8ft Copper-Bonded Steel Rods + Bentonite Slurry | 4 | Measured Earth Resistance < 2.5 Ohms | -- | $110.00 | $440.00 |

### 2.4 Cisco Networking & Rack Hardware
| Item # | Component Description | Manufacturer & Model | Qty | Unit Spec / Rating | Total Capacity | Unit Cost (USD) | Extended (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **NET-01**| Cisco Catalyst 3560-X / 3750-X Layer 3 Gigabit Core Switch | Cisco WS-C3560X-24P-L (24x GbE PoE+, IP Base) | 1 | 24x 10/100/1000 PoE+ ports, 435W PoE budget, 160 Gbps | -- | $480.00 | $480.00 |
| **NET-02**| Cisco Catalyst 2960-X Series 24-Port Gigabit Switches | Cisco WS-C2960X-24TS-L (LAN Base, 4x 1G SFP) | 3 | 24x GbE, 802.1Q, Port Security, DAI, DHCP Snooping | -- | $340.00 | $1,020.00 |
| **NET-03**| Cisco 2911 Integrated Services Routers (ISR G2) | Cisco CISCO2911/K9 (3x GE, 4x EHWIC, SEC-K9) | 2 | Hardware crypto acceleration, OSPFv2/v3, Zone Firewall | -- | $310.00 | $620.00 |
| **NET-04**| Cisco 2-Port Serial WAN Interface Cards | Cisco HWIC-2T (High-Speed Serial Synchronous/Async) | 4 | For point-to-point leased line & CCNA serial lab topology| -- | $45.00 | $180.00 |
| **NET-05**| 19" 42U Standard Server Rack with Dual Perforated Doors | APC NetShelter SX 42U Server Enclosure | 1 | Lockable mesh doors, PDU mounts, grounding kit | -- | $850.00 | $850.00 |
| **NET-06**| 24-Port Cat6 Unshielded Patch Panels & Cable Management | CommScope NETCONNECT Cat6 1U 110-Type | 4 | T568A/B universal wiring, horizontal cable managers | -- | $55.00 | $220.00 |
| **NET-07**| 1000ft Cat6 UTP 23AWG Solid Copper Network Cable Reel | Schneider Electric Acti9 / D-Link Solid Bare Copper | 3 | Fluke Channel Test Passed, low smoke zero halogen | -- | $160.00 | $480.00 |
| **NET-08**| FTDI USB to RJ45 Cisco Console Rollover Cables | FTDI Chipset FT232R USB 2.0 to RJ45 Console | 16 | For student terminal serial debugging pods | -- | $12.00 | $192.00 |

### 2.5 Student Computing Workstations & Uplinks
| Item # | Component Description | Manufacturer & Model | Qty | Unit Spec / Rating | Total Capacity | Unit Cost (USD) | Extended (USD) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **IT-01** | Ultra-Low Power Thin Client Workstations (Energy Saving) | HP ProDesk 405 G6 Mini / Lenovo ThinkCentre M75q | 30 | AMD Ryzen 5 Pro (6C/12T), 16GB DDR4, 256GB NVMe, 25W TDP | -- | $285.00 | $8,550.00 |
| **IT-02** | Energy Star 23.8" Full HD 1080p IPS LED Monitors | Dell E2422HS / HP P24v G4 (16W typical consumption) | 30 | 1920x1080 @ 60Hz, HDMI/VGA, Low Blue Light mode | -- | $115.00 | $3,450.00 |
| **IT-03** | Starlink High Performance Business Satellite Terminal | Starlink Business Kit (Flat High Performance Dishy) | 1 | 150-250 Mbps down, 25-40 Mbps up, heated snow/dust melt| -- | $1,800.00 | $1,800.00 |
| **IT-04** | Dual-SIM Industrial 4G/LTE Failover WAN Router | MikroTik Chateau LTE12 (Cat12 LTE, 5x GbE ports) | 1 | MTN Nigeria + Airtel Nigeria load balancing & failover | -- | $240.00 | $240.00 |
| **IT-05** | Enterprise Wi-Fi 6 Access Points (PoE powered) | Ubiquiti UniFi U6-Pro / Cisco Catalyst 9105AX | 2 | 802.11ax Dual-Band, 4x4 MU-MIMO, powered via 3560-X | -- | $160.00 | $320.00 |
| **IT-06** | Environmental Positive-Pressure Fan Unit with HEPA Filter | Noctua Industrial DC Fans + Washable Harmattan Filter | 2 | Keeps lab positive-pressure against fine Saharan sand | -- | $140.00 | $280.00 |

---

## 3. Financial Summary & Per-Seat Unit Economics

*Exchange Rate Baseline: 1 USD = 1,600 NGN (October 2026 Reference)*

| Category | Cost in USD ($) | Cost in NGN (₦) | Percentage of Budget |
| :--- | :--- | :--- | :--- |
| **1. Solar PV Generation Subsystem** | $5,104.00 | ₦8,166,400 | 14.3% |
| **2. Power Conversion & LiFePO4 Storage** | $11,740.00 | ₦18,784,000 | 32.9% |
| **3. AC Electrical Distribution & SPDs** | $1,592.00 | ₦2,547,200 | 4.5% |
| **4. Cisco Networking Pod Hardware** | $3,742.00 | ₦5,987,200 | 10.5% |
| **5. Student Workstations & Uplinks** | $14,640.00 | ₦23,424,000 | 41.0% |
| **Total Turnkey Capital Expenditure (CapEx)** | **$36,818.00** | **₦58,908,800** | **100.0%** |

### Per-Seat Capital Efficiency
* **Total Student Capacity**: 30 simultaneous physical workstations x 2 daily cohort shifts = **60 concurrent active students per term** (120 students annually).
* **Capital Cost per Concurrent Seat**: $\$36,818 \div 30 \text{ stations} = \mathbf{\$1,227.27}$.
* **Capital Cost per Trained Student (Annual Cohort)**: $\$36,818 \div 120 \text{ students} = \mathbf{\$306.82}$.
* **Marginal Operational Cost per Student (Monthly)**: **$24.50** (Covering Starlink satellite bandwidth, equipment maintenance, and terminal tooling).

---

## 4. Power Balance & Battery Autonomy Engineering Calculations

### 4.1 Daily Energy Consumption Profile (Full Lab Shift: 8 Hours)
$$\text{Workstations (30x Thin Clients @ 22W)} = 660 \text{ W}$$
$$\text{Monitors (30x LED @ 16W)} = 480 \text{ W}$$
$$\text{Cisco Rack (1x 3560X + 3x 2960X + 2x 2911 + 2x APs)} = 460 \text{ W}$$
$$\text{Uplink & IoT (Starlink Dishy 75W + MikroTik 15W + Telemetry 10W)} = 100 \text{ W}$$
$$\text{Ventilation & LED Lighting} = 220 \text{ W}$$
$$\mathbf{\text{Total Continuous Operating Load}} = \mathbf{1,920 \text{ W (1.92 kW)}}$$

$$\text{Daily Lab Energy Demand (8-hour operational cycle)} = 1.92 \text{ kW} \times 8 \text{ hours} = \mathbf{15.36 \text{ kWh / day}}$$

### 4.2 Solar PV Generation Budget (Maiduguri Location)
$$\text{Installed Array Peak Power} = 10.90 \text{ kWp}$$
$$\text{Minimum Maiduguri Peak Sun Hours (Worst-case Harmattan Season)} = 5.2 \text{ hours}$$
$$\text{System Derating Factor (Temperature, Inverter Loss, Dust Derating: 0.78)} = 0.78$$
$$\mathbf{\text{Expected Daily Solar PV Yield}} = 10.90 \text{ kWp} \times 5.2 \text{ PSH} \times 0.78 = \mathbf{44.21 \text{ kWh / day}}$$

$$\text{Daily Energy Surplus} = 44.21 \text{ kWh} - 15.36 \text{ kWh} = \mathbf{+28.85 \text{ kWh / day}}$$
*(The substantial energy surplus guarantees that the 28.8 kWh LiFePO4 battery bank is fully replenished to 100% SoC by 12:30 PM daily, providing reserve power for night classes and extended overcast monsoon days).*

### 4.3 Autonomous Battery Runtime Without Sunlight (Zero PV Generation)
$$\text{Total Nominal Battery Bank Capacity} = 28.8 \text{ kWh}$$
$$\text{Usable Capacity at 85% Maximum Depth of Discharge (DoD)} = 28.8 \text{ kWh} \times 0.85 = \mathbf{24.48 \text{ kWh}}$$
$$\text{Continuous Normal Load (1.92 kW)} \rightarrow \frac{24.48 \text{ kWh}}{1.92 \text{ kW}} = \mathbf{12.75 \text{ Hours Continuous Operation}}$$
$$\text{Stage 2 Conserve Load (0.95 kW)} \rightarrow \frac{24.48 \text{ kWh}}{0.95 \text{ kW}} = \mathbf{25.76 \text{ Hours Continuous Operation}}$$
$$\text{Stage 3 Critical Survival Load (0.24 kW)} \rightarrow \frac{24.48 \text{ kWh}}{0.24 \text{ kW}} = \mathbf{102.0 \text{ Hours (4.25 Days Uptime)}}$$
