# Port Scanner CLI

This is a simple, multi-threaded TCP port scanner written in Python. It is designed to find open ports on a target host.

## Features

*   Scans a target host (IP address or hostname).
*   Supports scanning a range of ports, a list of ports, or a single port.
*   Uses multiple threads for faster scanning.
*   Clear and simple output of open ports.

## Prerequisites

*   Python 3.6+
*   No external libraries are required.

## How to Run

1.  **Navigate to the project directory.**
    Ensure you have the `port_scanner_main.py` script and the `port_scanner` directory.

2.  **Run the application from your terminal.**
    Provide the target host and optionally a port range.

    ```bash
    python port_scanner_main.py <target_host> [options]
    ```

### Command-Line Options

*   `host`: (Required) The target host to scan (e.g., `127.0.0.1`, `example.com`).
*   `-p, --ports`: (Optional) The port range to scan. Defaults to `1-1024`.
    *   Formats:
        *   Range: `1-65535`
        *   Comma-separated list: `80,443,8080`
        *   Single port: `22`
*   `-t, --threads`: (Optional) The number of threads to use for scanning. Defaults to `20`.

### Example Usage

**Scan the default port range (1-1024) on localhost:**
```bash
python port_scanner_main.py 127.0.0.1
```

**Scan a specific range of ports on a remote host:**
```bash
python port_scanner_main.py example.com -p 1-200
```

**Scan specific ports:**
```bash
python port_scanner_main.py example.com --ports 22,80,443
```

**Increase the number of threads for a faster scan:**
```bash
python port_scanner_main.py scanme.nmap.org -t 50
```

**Example Output:**
```
Scanning host scanme.nmap.org for open ports...

--- Open Ports Found! ---
  [+] Port 22 is open
  [+] Port 80 is open
```

## Disclaimer

*   **LEGALITY**: Unauthorized port scanning of networks is illegal in many countries. This tool is intended for educational purposes and for use on networks where you have explicit permission to conduct scanning. The user assumes all liability for any misuse of this tool.
*   **ACCURACY**: The accuracy of the scan can be affected by firewalls, intrusion detection systems (IDS), and network latency. A port that is reported as closed may be filtered or blocked.
*   **PERFORMANCE**: Scanning a large range of ports can take a significant amount of time, even with multiple threads.

## File Structure
```
.
├── port_scanner_main.py            # Main CLI application script
├── port_scanner/
│   ├── __init__.py               # Makes port_scanner a Python package
│   └── scanner.py                # Core logic for port scanning
└── README_port_scanner.md          # This documentation file
```
