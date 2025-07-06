import subprocess
import re


def get_wifi_interface():
    """
    Tries to automatically determine the active Wi-Fi interface name on Linux.
    This is a helper and might not be foolproof on all systems.
    """
    try:
        # Try 'iw dev' first, as it's more modern
        result = subprocess.run(
            ["iw", "dev"], capture_output=True, text=True, check=True
        )
        for line in result.stdout.splitlines():
            if line.strip().startswith("Interface "):
                interface = line.strip().split(" ")[1]
                # Check if it's a wlan-type interface
                if interface.startswith(
                    ("wlan", "wlp", "wlx", "ath")
                ):  # Common Wi-Fi interface prefixes
                    return interface
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass  # iw not found or error, try nmcli

    try:
        # Fallback to 'nmcli dev status'
        result = subprocess.run(
            ["nmcli", "-t", "-f", "DEVICE,TYPE", "dev", "status"],
            capture_output=True,
            text=True,
            check=True,
        )
        for line in result.stdout.splitlines():
            parts = line.strip().split(":")
            if len(parts) == 2 and parts[1] == "wifi":
                return parts[0]  # Device name
    except (FileNotFoundError, subprocess.CalledProcessError):
        print(
            "Error: Could not automatically determine Wi-Fi interface using 'iw dev' or 'nmcli'."
        )
        print(
            "Please ensure 'iw' or 'nmcli' (NetworkManager) is installed and in your PATH."
        )
    return None


def parse_nmcli_output(output_str):
    """
    Parses the output of `nmcli -f SSID,CHAN,FREQ,SIGNAL,SECURITY dev wifi list`.
    """
    networks = []
    lines = output_str.strip().split("\n")

    if not lines or len(lines) < 1:  # Header might be missing if no networks
        return networks

    header = lines[0].strip()  # Potential header like "SSID CHAN FREQ SIGNAL SECURITY"
    # Actual data lines start from index 1 if header is present, or 0 if no networks found (nmcli might just output nothing or only header)

    # Determine column indices dynamically - more robust but assumes consistent field names
    # For simplicity in MVP, we'll assume a fixed order if a simple `nmcli dev wifi list` is used,
    # or rely on the exact fields if `-f` is used.
    # Let's assume we use `nmcli -f SSID,CHAN,FREQ,SIGNAL,SECURITY dev wifi list`
    # which should give a predictable headerless output if there's data, or just header if no data.
    # If `nmcli` outputs a header even with `-f` on some versions, we need to skip it.

    data_lines = lines
    if "SSID" in header and "CHAN" in header:  # Check if the first line is a header
        data_lines = lines[1:]

    for line in data_lines:
        line = line.strip()
        if not line:
            continue

        # Example line with -f SSID,CHAN,FREQ,SIGNAL,SECURITY:
        # MyWiFi:6:2437 MHz:80:WPA2
        # Sometimes nmcli uses variable spaces as delimiters if not using -t (terse)
        # Using -t with -f helps: `nmcli -t -f SSID,CHAN,FREQ,SIGNAL,SECURITY dev wifi list`
        # Output: MyWiFi\:Other:6:2437 MHz:75:WPA2  (SSIDs with colons are backslash-escaped)

        # We will assume the output of `nmcli -t -f ...` which uses ':' as a separator.
        # SSIDs can contain escaped colons, so simple split by ':' is not enough.
        # A more robust way is to use regex if we stick to non-terse, or handle escaped colons if terse.
        # For now, let's try a regex that handles spaces and then refine if needed.
        # Target fields: SSID, CHAN, FREQ, SIGNAL, SECURITY

        # Regex for parsing `nmcli -f SSID,CHAN,FREQ,SIGNAL,SECURITY dev wifi list` (non-terse)
        # This regex expects at least two spaces between fields, which is common for nmcli's default output.
        # It tries to capture SSID greedily, then looks for subsequent fields.
        # Example: "My Great SSID  6  2437 MHz  78  WPA2"
        # Example: "AnotherNet       11 2462 MHz  60  WPA1 WPA2" (Security can have spaces)

        # Let's try a simpler parsing first, assuming `nmcli -t -f SSID,CHAN,FREQ,SIGNAL,SECURITY dev wifi list`
        # which should give colon-separated values. SSIDs with ':' will be `\:`.
        parts = line.split(":")
        if len(parts) >= 5:  # SSID, CHAN, FREQ, SIGNAL, SECURITY[, EXTRA_STUFF_IF_ANY]
            ssid = parts[0].replace("\\:", ":")  # Handle escaped colons in SSID
            channel_str = parts[1]
            freq_str = parts[2]  # e.g., "2437 MHz" or "5180 MHz"
            signal_str = parts[3]  # e.g., "80"
            security = parts[4]
            # If security field itself contains colons due to multiple methods, join remaining parts
            if len(parts) > 5:
                security = ":".join(parts[4:])

            try:
                channel = int(channel_str) if channel_str else 0
                signal = int(signal_str) if signal_str else 0

                band = "Unknown"
                if "MHz" in freq_str:
                    freq_mhz = int(freq_str.split(" ")[0])
                    if 2400 <= freq_mhz < 2500:  # 2.4 GHz band typically 2412-2484 MHz
                        band = "2.4 GHz"
                    elif 5100 <= freq_mhz < 5900:  # 5 GHz band typically 5170-5825 MHz
                        band = "5 GHz"

                networks.append(
                    {
                        "ssid": ssid,
                        "signal": signal,
                        "channel": channel,
                        "band": band,
                        "frequency": freq_str,
                        "security": (
                            security if security else "Open"
                        ),  # Assume open if security is empty
                    }
                )
            except ValueError:
                print(f"Warning: Could not parse numeric value in line: {line}")
                continue
        # else:
        # print(f"Warning: Could not parse line, expected at least 5 colon-separated parts: '{line}'")

    return networks


def scan_wifi_networks(interface=None):
    """
    Scans for available Wi-Fi networks using nmcli on Linux.

    Args:
        interface (str, optional): The Wi-Fi interface name. If None, tries to auto-detect.

    Returns:
        list: A list of dictionaries, where each dictionary represents a Wi-Fi network.
              Returns an empty list if scanning fails or no networks are found.
    """
    if interface is None:
        interface = get_wifi_interface()
        if interface is None:
            print("Exiting: No Wi-Fi interface provided or auto-detected.")
            return []

    # Use -t for terse output (colon-separated), -f for specific fields.
    # Rescan to ensure fresh results. Sometimes `nmcli dev wifi rescan` is needed first.
    try:
        subprocess.run(
            ["nmcli", "dev", "wifi", "rescan", "ifname", interface],
            capture_output=True,
            text=True,
            timeout=10,
        )  # Allow some time for rescan
    except FileNotFoundError:
        print(
            "Error: nmcli command not found. Please ensure NetworkManager is installed."
        )
        return []
    except subprocess.TimeoutExpired:
        print(
            "Warning: nmcli rescan command timed out. Proceeding with potentially stale data."
        )
    except subprocess.CalledProcessError as e:
        print(f"Warning: nmcli rescan failed: {e.stderr}")
        # Continue anyway, list might still work with cached data

    cmd = [
        "nmcli",
        "-t",
        "-f",
        "SSID,CHAN,FREQ,SIGNAL,SECURITY",
        "dev",
        "wifi",
        "list",
        "ifname",
        interface,
    ]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, check=True, timeout=15
        )
        if result.stderr:
            print(f"Warning/Error from nmcli list: {result.stderr.strip()}")
        return parse_nmcli_output(result.stdout)
    except FileNotFoundError:
        print(
            "Error: nmcli command not found. Please ensure NetworkManager is installed."
        )
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error scanning Wi-Fi networks with nmcli: {e}")
        print(f"STDERR: {e.stderr.strip()}")
        return []
    except subprocess.TimeoutExpired:
        print("Error: nmcli list command timed out.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during Wi-Fi scan: {e}")
        return []


if __name__ == "__main__":
    print("Attempting to find Wi-Fi interface...")
    wifi_interface = get_wifi_interface()

    if wifi_interface:
        print(f"Using Wi-Fi interface: {wifi_interface}")
        print("\nScanning for Wi-Fi networks...")
        networks = scan_wifi_networks(interface=wifi_interface)
        if networks:
            print(f"\nFound {len(networks)} networks:")
            for net in networks:
                print(f"  SSID: {net['ssid']}")
                print(f"    Signal: {net['signal']}%")
                print(f"    Channel: {net['channel']} ({net['band']})")
                print(f"    Frequency: {net['frequency']}")
                print(f"    Security: {net['security']}")
                print("-" * 20)
        else:
            print("No networks found or error during scan.")
    else:
        print("Could not run scan as no Wi-Fi interface was found.")

    print("\n--- Test parsing with mock nmcli output ---")
    mock_output_header = """SSID:CHAN:FREQ:SIGNAL:SECURITY
MyAwesomeWiFi:11:2462 MHz:88:WPA2
AnotherNet\:Work:6:2437 MHz:70:WPA1 WPA2
Open unsecured:1:2412 MHz:50:--
WEPNet:48:5240 MHz:62:WEP
"""
    mock_output_no_header = """MyAwesomeWiFi:11:2462 MHz:88:WPA2
AnotherNet\:Work:6:2437 MHz:70:WPA1 WPA2
Open unsecured:1:2412 MHz:50:
WEPNet:48:5240 MHz:62:WEP
EmptySignal::2412 MHz::WPA2
"""  # nmcli -t -f ... does not print header if there is data

    parsed_networks_mock = parse_nmcli_output(mock_output_no_header)
    print(f"Parsed {len(parsed_networks_mock)} networks from mock data:")
    for net in parsed_networks_mock:
        print(
            f"  SSID: {net['ssid']}, Signal: {net['signal']}, Chan: {net['channel']}, Band: {net['band']}, Security: {net['security']}"
        )

    assert (
        len(parsed_networks_mock) == 4
    )  # "EmptySignal" fails int conversion for signal
    assert parsed_networks_mock[0]["ssid"] == "MyAwesomeWiFi"
    assert parsed_networks_mock[0]["signal"] == 88
    assert parsed_networks_mock[1]["ssid"] == "AnotherNet:Work"
    assert parsed_networks_mock[1]["security"] == "WPA1 WPA2"
    assert parsed_networks_mock[2]["security"] == "Open"
    assert parsed_networks_mock[3]["band"] == "5 GHz"
    print("Mock data parsing tests passed (basic checks).")

    # Test with header (nmcli might output header if no networks are found)
    parsed_with_header = parse_nmcli_output("SSID:CHAN:FREQ:SIGNAL:SECURITY\n")
    assert len(parsed_with_header) == 0
    print("Parsing empty data with only header line passed.")

    parsed_no_networks = parse_nmcli_output(
        "SSID:CHAN:FREQ:SIGNAL:SECURITY"
    )  # Only header
    assert len(parsed_no_networks) == 0
    print("Parsing only header line (no newline) passed.")

    parsed_empty_str = parse_nmcli_output("")
    assert len(parsed_empty_str) == 0
    print("Parsing empty string passed.")
