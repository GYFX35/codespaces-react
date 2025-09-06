import argparse
import sys
from port_scanner import scanner

def main():
    parser = argparse.ArgumentParser(description="A simple TCP port scanner.")
    parser.add_argument("host", help="The target host to scan (IP address or hostname).")
    parser.add_argument("-p", "--ports", dest="port_range", default="1-1024",
                        help="Port range to scan (e.g., '1-1024', '80,443', '22'). Defaults to '1-1024'.")
    parser.add_argument("-t", "--threads", dest="threads", type=int, default=20,
                        help="Number of threads to use for scanning. Defaults to 20.")
    args = parser.parse_args()

    target_host = args.host
    port_range_str = args.port_range
    num_threads = args.threads

    ports_to_scan = []
    try:
        # Handle different formats like '1-1024' or '80,443' or '22'
        if '-' in port_range_str:
            start, end = map(int, port_range_str.split('-'))
            ports_to_scan = range(start, end + 1)
        elif ',' in port_range_str:
            ports_to_scan = [int(p.strip()) for p in port_range_str.split(',')]
        else:
            ports_to_scan = [int(port_range_str)]
    except ValueError:
        print(f"Error: Invalid port range format '{port_range_str}'. Use formats like '1-1024', '80,443', or '22'.")
        sys.exit(1)

    print(f"Scanning host {target_host} for open ports...")

    # In this implementation, we will pass the start and end of the main range.
    # A more complex implementation would handle disjointed lists of ports.
    start_port = min(ports_to_scan)
    end_port = max(ports_to_scan)

    open_ports = scanner.scan_ports(target_host, start_port, end_port, max_workers=num_threads)

    if not open_ports:
        print("\n--- No Open Ports Found ---")
        print(f"No open ports were found in the specified range on {target_host}.")
    else:
        print("\n--- Open Ports Found! ---")
        for port in open_ports:
            print(f"  [+] Port {port} is open")

if __name__ == "__main__":
    main()
