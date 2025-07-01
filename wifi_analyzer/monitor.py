import subprocess
import time
import re

def get_current_connection_info_nmcli(interface):
    """
    Gets current connection details using 'nmcli dev show <interface>'.
    Parses for SSID and signal strength.
    """
    try:
        cmd = ['nmcli', '-t', '-f', 'GENERAL.CONNECTION,WIFI.SSID,WIFI.SIGNAL', 'dev', 'show', interface]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=5)

        ssid = "N/A"
        signal = 0
        connection_name = "N/A"

        for line in result.stdout.strip().split('\n'):
            if line.startswith("GENERAL.CONNECTION:"):
                connection_name = line.split(':', 1)[1].replace('\\:', ':')
            elif line.startswith("WIFI.SSID:") or line.startswith("802-11-wireless.ssid:"): # Some versions use different prefix
                ssid = line.split(':', 1)[1].replace('\\:', ':')
            elif line.startswith("WIFI.SIGNAL:") or line.startswith("802-11-wireless.signal:"):
                signal_str = line.split(':', 1)[1]
                if signal_str.isdigit():
                    signal = int(signal_str)

        if connection_name == "--" or not connection_name : # '--' means not connected or no active connection name
             if ssid == "--" or not ssid: # Double check if SSID was also empty or '--'
                return None # Not connected or no info

        # If SSID is still empty but connection name exists, it might be a non-Wi-Fi connection or nmcli version difference
        # For Wi-Fi, SSID should generally be present if connected.
        if not ssid or ssid == "--": # If SSID is explicitly "--" or empty, treat as not connected to Wi-Fi for our purpose
            return None

        return {"ssid": ssid, "signal": signal, "connection_name": connection_name}

    except FileNotFoundError:
        print("Error: nmcli command not found for current connection info.")
        return None
    except subprocess.CalledProcessError:
        # This can happen if the interface doesn't exist or isn't Wi-Fi, or other nmcli errors
        # print(f"Error getting connection info for {interface} via nmcli: {e.stderr}")
        return None # Indicates not connected or error
    except subprocess.TimeoutExpired:
        print(f"Timeout getting connection info for {interface} via nmcli.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while getting current connection info with nmcli: {e}")
        return None

def get_current_signal_strength_iw(interface):
    """
    Gets current signal strength using 'iw dev <interface> link'.
    Parses for SSID and signal strength (dBm).
    Note: This usually requires sudo if not already granted for iw.
    However, `iw dev <iface> link` often works without sudo for current link.
    """
    try:
        cmd = ['iw', 'dev', interface, 'link']
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=5)

        ssid = "N/A"
        signal_dbm = None # Typically a negative value like -50

        lines = result.stdout.strip().split('\n')
        if lines[0].strip().startswith(f"Not connected."): # Check first line for "Not connected."
            return None

        for line in lines:
            if line.strip().startswith("SSID:"):
                ssid = line.split("SSID:", 1)[1].strip()
            elif "signal:" in line:
                match = re.search(r"signal:\s*(-?\d+)\s*dBm", line)
                if match:
                    signal_dbm = int(match.group(1))

        if ssid == "N/A" and signal_dbm is None: # If neither was found, likely not connected
            return None

        return {"ssid": ssid, "signal_dbm": signal_dbm}

    except FileNotFoundError:
        print("Error: iw command not found for current signal strength.")
        return None
    except subprocess.CalledProcessError:
        # This can happen if the interface is not connected or other iw errors
        # print(f"Error getting signal strength for {interface} via iw: {e.stderr}")
        return None
    except subprocess.TimeoutExpired:
        print(f"Timeout getting signal strength for {interface} via iw.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred while getting current signal strength with iw: {e}")
        return None


def monitor_current_connection_signal(interface, duration=10, interval=2, use_iw=False):
    """
    Monitors and displays the signal strength of the current Wi-Fi connection.

    Args:
        interface (str): The Wi-Fi interface name.
        duration (int): How long to monitor in seconds.
        interval (int): How often to check the signal in seconds.
        use_iw (bool): If True, try to use 'iw' for signal strength (dBm). Otherwise, use 'nmcli'.
    """
    print(f"\n--- Monitoring Signal Strength for Current Connection on '{interface}' ---")
    print(f"Monitoring for {duration} seconds (updates every {interval}s). Press Ctrl+C to stop early.")

    end_time = time.time() + duration
    try:
        while time.time() < end_time:
            info = None
            if use_iw:
                info = get_current_signal_strength_iw(interface)
                if info:
                    print(f"SSID: {info['ssid']}, Signal: {info['signal_dbm']} dBm")
                else:
                    print("Not connected or unable to fetch signal via iw.")
            else: # use nmcli
                info = get_current_connection_info_nmcli(interface)
                if info:
                    print(f"SSID: {info['ssid']}, Signal Quality: {info['signal']}% (Connection: {info['connection_name']})")
                else:
                    print("Not connected or unable to fetch signal via nmcli.")

            # Wait for the next interval, but check frequently for Ctrl+C
            for _ in range(interval * 10): # Check 10 times per second for interval
                if time.time() >= end_time:
                    break
                time.sleep(0.1)
            if time.time() >= end_time:
                    break
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")
    except Exception as e:
        print(f"\nAn error occurred during monitoring: {e}")
    finally:
        print("Monitoring finished.")


if __name__ == '__main__':
    # This import is only for the __main__ block to reuse get_wifi_interface
    from .scanner import get_wifi_interface

    print("Attempting to find Wi-Fi interface for monitoring...")
    wifi_interface = get_wifi_interface()

    if wifi_interface:
        print(f"Using Wi-Fi interface: {wifi_interface}")

        print("\n--- Testing nmcli for current connection info ---")
        nmcli_info = get_current_connection_info_nmcli(wifi_interface)
        if nmcli_info:
            print(f"nmcli - SSID: {nmcli_info['ssid']}, Signal: {nmcli_info['signal']}%, Connection: {nmcli_info['connection_name']}")
        else:
            print("nmcli - Not connected or no info retrieved.")

        print("\n--- Testing iw for current connection info ---")
        iw_info = get_current_signal_strength_iw(wifi_interface)
        if iw_info:
            print(f"iw - SSID: {iw_info['ssid']}, Signal: {iw_info['signal_dbm']} dBm")
        else:
            print("iw - Not connected or no info retrieved.")

        # Example of running the monitor
        # Choose one method for the actual monitoring call, or allow user to choose in a real CLI
        # For testing, we'll prefer nmcli if available as it doesn't usually need sudo.

        # To actually run monitoring for a short period:
        # print("\n--- Starting live monitor test (nmcli) ---")
        # monitor_current_connection_signal(wifi_interface, duration=6, interval=2, use_iw=False)

        # print("\n--- Starting live monitor test (iw) ---")
        # monitor_current_connection_signal(wifi_interface, duration=6, interval=2, use_iw=True)

    else:
        print("Could not run monitoring tests as no Wi-Fi interface was found.")

    print("\n--- Mock Test: nmcli parsing ---")
    mock_nmcli_output_connected = """GENERAL.CONNECTION:MyHomeWiFi
WIFI.SSID:MyHomeWiFi
WIFI.SIGNAL:85
"""
    mock_nmcli_output_not_connected = "GENERAL.CONNECTION:--\nWIFI.SSID:--\nWIFI.SIGNAL:0\n"
    # Simulate subprocess run for parsing test
    class MockCompletedProcess:
        def __init__(self, stdout, stderr="", returncode=0):
            self.stdout = stdout
            self.stderr = stderr
            self.returncode = returncode
        def check_returncode(self):
            if self.returncode != 0:
                raise subprocess.CalledProcessError(self.returncode, "cmd", output=self.stdout, stderr=self.stderr)

    original_subprocess_run = subprocess.run # Save original

    # Mock for connected state
    def mock_run_connected(*args, **kwargs):
        return MockCompletedProcess(mock_nmcli_output_connected)
    subprocess.run = mock_run_connected
    parsed_info = get_current_connection_info_nmcli("wlan_mock")
    assert parsed_info is not None
    assert parsed_info["ssid"] == "MyHomeWiFi"
    assert parsed_info["signal"] == 85
    print("Mock nmcli (connected) parsing: PASS")

    # Mock for not connected state
    def mock_run_not_connected(*args, **kwargs):
        return MockCompletedProcess(mock_nmcli_output_not_connected)
    subprocess.run = mock_run_not_connected
    parsed_info_nc = get_current_connection_info_nmcli("wlan_mock_nc")
    assert parsed_info_nc is None
    print("Mock nmcli (not connected) parsing: PASS")

    subprocess.run = original_subprocess_run # Restore original

    print("\n--- Mock Test: iw parsing ---")
    mock_iw_output_connected = """Connected to aa:bb:cc:dd:ee:ff (on wlan_mock)
	SSID: MyIWNetwork
	freq: 2412
	RX: 12345 bytes (100 packets)
	TX: 6789 bytes (50 packets)
	signal: -55 dBm
	tx bitrate: 72.2 MBit/s
"""
    mock_iw_output_not_connected = "Not connected."

    # Mock for iw connected
    def mock_run_iw_connected(*args, **kwargs):
        return MockCompletedProcess(mock_iw_output_connected)
    subprocess.run = mock_run_iw_connected
    parsed_iw_info = get_current_signal_strength_iw("wlan_mock_iw")
    assert parsed_iw_info is not None
    assert parsed_iw_info["ssid"] == "MyIWNetwork"
    assert parsed_iw_info["signal_dbm"] == -55
    print("Mock iw (connected) parsing: PASS")

    # Mock for iw not connected
    def mock_run_iw_not_connected(*args, **kwargs):
        return MockCompletedProcess(mock_iw_output_not_connected)
    subprocess.run = mock_run_iw_not_connected
    parsed_iw_info_nc = get_current_signal_strength_iw("wlan_mock_iw_nc")
    assert parsed_iw_info_nc is None
    print("Mock iw (not connected) parsing: PASS")

    subprocess.run = original_subprocess_run # Restore original
```
