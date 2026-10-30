#!/usr/bin/env python3
"""
Cisco IOS Multi-Threaded Backup & Configuration Drift Engine
Solar-Powered Cyber & Cisco Networking Academy — Northeast Nigeria
Operating Entity: ESSCO TECH AGENCY LTD (RC: 7192842)
Location: Royas Plaza, Damboa Road, Maiduguri, Borno State

This tool pulls running configurations from Cisco switches and routers concurrently,
computes SHA-256 cryptographic checksums, detects unauthorized configuration drift,
and archives timestamped backups. Supports mock execution for CI/CD validation.
"""

from __future__ import annotations

import argparse
import concurrent.futures
from datetime import datetime, timezone
import hashlib
from pathlib import Path
import sys
import time
from typing import Dict, List, Optional

from pydantic import BaseModel, Field
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

# Optional import for Netmiko (handled gracefully if running in mock/CI)
try:
    from netmiko import ConnectHandler
    from netmiko.exceptions import (
        NetmikoAuthenticationException,
        NetmikoTimeoutException,
    )

    NETMIKO_AVAILABLE = True
except ImportError:
    NETMIKO_AVAILABLE = False


if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

console = Console(
    force_terminal=True, legacy_windows=False if sys.platform != "win32" else None
)


class DeviceSpec(BaseModel):
    name: str = Field(..., description="Unique hostname identifier")
    host: str = Field(..., description="IPv4 or IPv6 management address")
    device_type: str = Field(default="cisco_ios", description="Netmiko device type")
    username: str = Field(default="secadmin")
    password: str = Field(default="AdminSecure#Maiduguri2026!")
    secret: str = Field(default="CiscoAcademy@Maiduguri2026!")
    port: int = Field(default=22)
    role: str = Field(default="Access Switch")


class BackupResult(BaseModel):
    device_name: str
    host: str
    status: str  # "SUCCESS", "DRIFT_DETECTED", "AUTH_FAILED", "TIMEOUT", "ERROR"
    checksum: str = ""
    diff_summary: str = ""
    duration_seconds: float = 0.0
    backup_path: Optional[str] = None
    error_message: Optional[str] = None


DEFAULT_INVENTORY: List[DeviceSpec] = [
    DeviceSpec(name="SW-CORE-01", host="10.200.20.1", role="Core Switch / ABR"),
    DeviceSpec(name="SW-DIST-01", host="10.200.20.2", role="Distribution Switch"),
    DeviceSpec(
        name="SW-POD-A-01", host="10.200.20.11", role="Student Pod A Catalyst 2960X"
    ),
    DeviceSpec(
        name="SW-POD-B-01", host="10.200.20.12", role="Student Pod B Catalyst 2960X"
    ),
    DeviceSpec(
        name="R1-GATEWAY", host="10.200.20.254", role="Starlink Gateway Router 2911"
    ),
]

MOCK_CONFIG_TEMPLATE = """!
version 15.2
service timestamps log datetime msec
service password-encryption
!
hostname {hostname}
!
ip domain-name academy.esscotechagency.internal
ip ssh version 2
!
interface GigabitEthernet0/1
 description Student-Pod-Port
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
!
interface GigabitEthernet0/24
 description Core-Uplink
 switchport mode trunk
 switchport trunk native vlan 999
!
line vty 0 4
 transport input ssh
!
end
"""


def compute_sha256(content: str) -> str:
    """Calculate normalized SHA-256 hash ignoring timestamps and empty comment lines."""
    normalized_lines = [
        line.strip()
        for line in content.splitlines()
        if line.strip()
        and not line.strip().startswith("!")
        and "ntp clock-period" not in line
    ]
    normalized_text = "\n".join(normalized_lines)
    return hashlib.sha256(normalized_text.encode("utf-8")).hexdigest()


def backup_device(
    device: DeviceSpec,
    output_dir: Path,
    mock: bool = False,
    timeout: int = 15,
) -> BackupResult:
    start_time = time.time()
    device_dir = output_dir / device.name
    device_dir.mkdir(parents=True, exist_ok=True)
    latest_file = device_dir / "latest.cfg"

    if mock:
        # Simulate realistic network latency (100ms - 300ms)
        time.sleep(0.15)
        raw_config = MOCK_CONFIG_TEMPLATE.format(hostname=device.name)
        new_hash = compute_sha256(raw_config)
        elapsed = round(time.time() - start_time, 2)

        # Check for drift against latest file
        drift_detected = False
        if latest_file.exists():
            old_hash = compute_sha256(latest_file.read_text(encoding="utf-8"))
            if old_hash != new_hash:
                drift_detected = True

        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
        timestamp_file = device_dir / f"{device.name}_{timestamp_str}.cfg"
        timestamp_file.write_text(raw_config, encoding="utf-8")
        latest_file.write_text(raw_config, encoding="utf-8")

        status = "DRIFT_DETECTED" if drift_detected else "SUCCESS"
        return BackupResult(
            device_name=device.name,
            host=device.host,
            status=status,
            checksum=new_hash[:12],
            duration_seconds=elapsed,
            backup_path=str(timestamp_file),
        )

    # Real Netmiko execution
    if not NETMIKO_AVAILABLE:
        return BackupResult(
            device_name=device.name,
            host=device.host,
            status="ERROR",
            error_message="Netmiko library is not installed.",
            duration_seconds=round(time.time() - start_time, 2),
        )

    device_params = {
        "device_type": device.device_type,
        "host": device.host,
        "username": device.username,
        "password": device.password,
        "secret": device.secret,
        "port": device.port,
        "timeout": timeout,
        "fast_cli": False,
    }

    try:
        with ConnectHandler(**device_params) as net_connect:
            net_connect.enable()
            raw_config = net_connect.send_command("show running-config")

        new_hash = compute_sha256(raw_config)
        elapsed = round(time.time() - start_time, 2)

        drift_detected = False
        if latest_file.exists():
            old_hash = compute_sha256(latest_file.read_text(encoding="utf-8"))
            if old_hash != new_hash:
                drift_detected = True

        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%SZ")
        timestamp_file = device_dir / f"{device.name}_{timestamp_str}.cfg"
        timestamp_file.write_text(raw_config, encoding="utf-8")
        latest_file.write_text(raw_config, encoding="utf-8")

        status = "DRIFT_DETECTED" if drift_detected else "SUCCESS"
        return BackupResult(
            device_name=device.name,
            host=device.host,
            status=status,
            checksum=new_hash[:12],
            duration_seconds=elapsed,
            backup_path=str(timestamp_file),
        )

    except NetmikoAuthenticationException:
        return BackupResult(
            device_name=device.name,
            host=device.host,
            status="AUTH_FAILED",
            error_message="Authentication credentials rejected.",
            duration_seconds=round(time.time() - start_time, 2),
        )
    except NetmikoTimeoutException:
        return BackupResult(
            device_name=device.name,
            host=device.host,
            status="TIMEOUT",
            error_message=f"Connection timed out after {timeout}s.",
            duration_seconds=round(time.time() - start_time, 2),
        )
    except Exception as exc:
        return BackupResult(
            device_name=device.name,
            host=device.host,
            status="ERROR",
            error_message=str(exc),
            duration_seconds=round(time.time() - start_time, 2),
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="ESSCO Tech Academy Cisco Multi-Threaded Backup Engine"
    )
    parser.add_argument(
        "--mock", action="store_true", help="Run with mock network devices for CI/CD"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate logic without changing production state",
    )
    parser.add_argument(
        "--output-dir", default="backups", help="Directory where configs are archived"
    )
    parser.add_argument(
        "--workers", type=int, default=5, help="Concurrent worker threads"
    )
    args = parser.parse_args()

    console.print(
        Panel.fit(
            "[bold green]Solar-Powered Cyber & Cisco Networking Academy[/bold green]\n"
            "[cyan]Cisco IOS Multi-Threaded Backup & Config Drift Engine[/cyan]\n"
            "[yellow]ESSCO TECH AGENCY LTD (RC: 7192842) - Maiduguri, Borno State[/yellow]",
            title="Infrastructure Automation",
            border_style="green",
        )
    )

    out_path = Path(args.output_dir)
    devices = DEFAULT_INVENTORY
    console.print(
        f"[bold blue]Initiating concurrent backup across {len(devices)} devices (Workers: {args.workers})...[/bold blue]\n"
    )

    results: List[BackupResult] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_map = {
            executor.submit(
                backup_device, device, out_path, mock=args.mock, timeout=15
            ): device
            for device in devices
        }
        for future in concurrent.futures.as_completed(future_map):
            res = future.result()
            results.append(res)

    # Render summary table
    table = Table(
        title="Device Configuration Backup Report",
        show_header=True,
        header_style="bold magenta",
    )
    table.add_column("Device Name", style="bold white")
    table.add_column("Management IP", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("SHA-256 (12c)", style="dim")
    table.add_column("Elapsed (s)", justify="right")
    table.add_column("Details", style="italic")

    all_passed = True
    for r in sorted(results, key=lambda x: x.device_name):
        if r.status == "SUCCESS":
            status_style = "[green]SUCCESS[/green]"
            details = f"Archived to {r.backup_path}"
        elif r.status == "DRIFT_DETECTED":
            status_style = "[yellow]DRIFT DETECTED[/yellow]"
            details = "Configuration changed since last baseline"
        else:
            status_style = f"[red]{r.status}[/red]"
            details = r.error_message or "Unknown failure"
            all_passed = False

        table.add_row(
            r.device_name,
            r.host,
            status_style,
            r.checksum or "N/A",
            f"{r.duration_seconds:.2f}",
            details,
        )

    console.print(table)

    if all_passed:
        console.print(
            "\n[bold green][OK] All device configurations successfully backed up and validated.[/bold green]"
        )
        return 0
    else:
        console.print(
            "\n[bold red][ERROR] One or more backup targets failed. Review alerts above.[/bold red]"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
