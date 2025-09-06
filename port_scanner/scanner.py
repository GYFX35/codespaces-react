import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_port(host, port, timeout=0.5):
    """
    Scans a single port on a target host.

    Args:
        host (str): The target host IP address or hostname.
        port (int): The port to scan.
        timeout (float): Connection timeout in seconds.

    Returns:
        True if the port is open, False otherwise.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    try:
        s.connect((host, port))
        return True
    except (socket.timeout, ConnectionRefusedError, socket.gaierror, OSError):
        return False
    finally:
        s.close()

def scan_ports(host, start_port, end_port, max_workers=20):
    """
    Scans a range of ports on a target host using multiple threads.

    Args:
        host (str): The target host IP address or hostname.
        start_port (int): The starting port of the range.
        end_port (int): The ending port of the range.
        max_workers (int): The maximum number of threads to use.

    Returns:
        A sorted list of open ports.
    """
    open_ports = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Create a future for each port scan
        future_to_port = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}

        for future in as_completed(future_to_port):
            port = future_to_port[future]
            try:
                if future.result():
                    open_ports.append(port)
            except Exception as exc:
                # Can be useful for debugging if something goes wrong with a future
                pass

    return sorted(open_ports)
