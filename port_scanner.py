#!/usr/bin/env python3
"""
PORT SCANNER - Ethical Security Testing Tool
Author: [Your Name]
Date: [Today's Date]
LEGAL NOTICE: ONLY scan localhost (127.0.0.1) or scanme.nmap.org per assignment rules
"""

import socket
import sys
import argparse
import time
from datetime import datetime

def scan_port(host, port, timeout=1.0):
    """Scan single port - returns True if open, False if closed/filtered."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def validate_target(host):
    """Enforce ethical scanning rules - ONLY allow localhost or scanme.nmap.org."""
    allowed = ['127.0.0.1', 'localhost', 'scanme.nmap.org', '::1']
    host_clean = host.lower().strip()
    
    if host_clean not in allowed and not host_clean.startswith('127.'):
        print(f"\n[✗] ILLEGAL TARGET: {host}", file=sys.stderr)
        print("[!] Per assignment rules, you may ONLY scan:", file=sys.stderr)
        print("    • localhost (127.0.0.1)", file=sys.stderr)
        print("    • scanme.nmap.org (official test target)", file=sys.stderr)
        print("[!] Scanning unauthorized systems is ILLEGAL and violates course policy", file=sys.stderr)
        sys.exit(1)
    return host_clean

def scan_ports(host, start_port, end_port):
    """Scan port range with progress display and ethical safeguards."""
    host = validate_target(host)
    
    # Resolve hostname to IP
    try:
        ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"[✗] Cannot resolve hostname: {host}", file=sys.stderr)
        sys.exit(1)
    
    # Validate port range
    if not (1 <= start_port <= 65535) or not (1 <= end_port <= 65535):
        print("[✗] Invalid port range (must be 1-65535)", file=sys.stderr)
        sys.exit(1)
    if start_port > end_port:
        start_port, end_port = end_port, start_port  # Auto-correct reversed range
    
    # Display scan header
    print(f"\n{'='*70}")
    print(f" ETHICAL PORT SCANNER - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    print(f" Target: {host} ({ip})")
    print(f" Port Range: {start_port}-{end_port} (Total: {end_port - start_port + 1} ports)")
    print(f" Timeout: 1.0 second per port")
    print(f"{'='*70}\n")
    
    open_ports = []
    start_time = time.time()
    
    # Scan each port
    for port in range(start_port, end_port + 1):
        is_open = scan_port(host, port)
        
        # Visual progress indicator
        status = "OPEN  " if is_open else "closed"
        progress = (port - start_port + 1) / (end_port - start_port + 1) * 100
        bar = "█" * int(progress/2) + "-" * (50 - int(progress/2))
        
        print(f"\r[ {bar} ] {progress:5.1f}% | Port {port:5d}: {status}", end='', flush=True)
        
        if is_open:
            open_ports.append(port)
        
        # Ethical delay between scans (required for scanme.nmap.org)
        if host == 'scanme.nmap.org' and port != end_port:
            time.sleep(0.5)
    
    # Display results
    elapsed = time.time() - start_time
    print(f"\n\n{'='*70}")
    print(f" SCAN COMPLETE ({elapsed:.1f} seconds)")
    print(f"{'='*70}")
    
    if open_ports:
        print(f"\n[✓] OPEN PORTS FOUND ({len(open_ports)}):")
        for port in open_ports:
            service = {22: 'SSH', 80: 'HTTP', 443: 'HTTPS'}.get(port, 'Unknown')
            print(f"    • Port {port:5d} - {service}")
    else:
        print(f"\n[!] No open ports found in range {start_port}-{end_port}")
    
    print(f"\n{'='*70}\n")

def main():
    parser = argparse.ArgumentParser(description='Ethical Port Scanner (localhost/scanme.nmap.org ONLY)')
    parser.add_argument('host', help='Target: 127.0.0.1 or scanme.nmap.org')
    parser.add_argument('start_port', type=int, help='Start port (1-65535)')
    parser.add_argument('end_port', type=int, help='End port (1-65535)')
    args = parser.parse_args()
    
    scan_ports(args.host, args.start_port, args.end_port)

if __name__ == "__main__":
    main()